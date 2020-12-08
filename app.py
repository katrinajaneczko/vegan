#I used videos and sample code from https://cs50.harvard.edu/x/2020/tracks/web/ to help me develop this web app

from cs50 import SQL
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash 
from werkzeug.utils import secure_filename

from helpers import apology, login_required

import numpy, cv2, webbrowser, requests, json, os, base64
import pyzbar.pyzbar as pyzbar

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Specify directory to save uploaded images
app.config["IMAGE_UPLOADS"] = "/Users/katrinajaneczko/Downloads/vegan/static/uploads"

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///barcodes.db")


@app.route("/")
@login_required
def index():
    """Show homepage"""
    return render_template("index.html")

@app.route("/about")
@login_required
def about():
    """Show about page"""
    return render_template("about.html")


@app.route("/barcode", methods=["GET", "POST"])
@login_required
def barcode():
    """Look up barcode for information"""

    if request.method == "GET":
        return render_template("barcodeupload.html")

    else:
            
        def vegan_check(ingredients):

            #Create list of nonvegan ingredients from txt file of nonvegan ingredients
            nonvegan_file = open("static/not_vegan_list.txt", 'r').readlines()
            nonvegan = []
            for line in nonvegan_file:
                line = line.strip("\n").upper()
                nonvegan.append(line)

            #Create list of vegan ingredient "exceptions" from txt file
            vegan_file = open("static/vegan_exceptions_list.txt", 'r').readlines()
            exceptions = []
            for line in vegan_file:
                line = line.strip("\n").upper()
                exceptions.append(line)
            print(exceptions)

            #Tidy up the ingredients into a list, split into entries by commas
            ingredients = ingredients.replace(".", ",").replace("(" , ",").replace("[" , ",").replace(")" , "").replace("]" , "").split(",")

            #Strip irrelevant words 
            strip_words = ['AND', 'CONTAINS LESS THAN 1% OF', 'CONTAINS LESS THAN 2% OF']
            for i, entry in enumerate(ingredients):
                entry = entry.strip("   ").strip("*")
                for strip_word in strip_words:
                    if entry.startswith(strip_word):
                        entry = entry.replace(strip_word, "").strip(" :- ")
                ingredients[i] = entry

            #Check each ingredient of product against nonvegan list and determine if vegan or not
            for ingredient in ingredients:
                for item in nonvegan:
                    if item in ingredient and ("vegan" not in ingredient and ingredient not in exceptions):
                        reason = ingredient
                        return ["No", reason]
            return ["Yes", None]

        #I used https://pypi.org/project/opencv-python/ and https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_image_display/py_image_display.html and https://www.pyimagesearch.com/2014/11/24/detecting-barcodes-images-python-opencv/ and https://stackoverflow.com/questions/47515243/reading-image-file-file-storage-object-using-cv2 to use cv2 to create the barcode reader
        def modify(uploaded_img_cv, decoded_object): #arg types: cv2 numpy.ndarray, list; return type: str?
            """Take original uploaded image file and return a new image with a drawn a rectangle around the barcode"""

            #Draw rectangle on image
            points = decoded_object[0].rect
            modified_img_cv = cv2.rectangle(uploaded_img_cv, (points.left, points.top), 
                                        (points.left + points.width, points.top + points.height),
                                        color=(0, 255, 0),
                                        thickness=5) 

            #Convert numpy array to bytes/b64
            #modified_img_cv = cv2.resize(modified_img_cv, (64, 64), cv2.INTER_NEAREST)
            _, modified_img_jpg = cv2.imencode('.jpg', modified_img_cv)  # im_arr: image in Numpy one-dim array format.
            modified_img_bytes = modified_img_jpg.tobytes()
            modified_img_b64 = base64.b64encode(modified_img_bytes)

            return "data:image/jpg;base64," + modified_img_b64.decode('ascii')
            

        #Retrieve image file from form, read image file string data
        uploaded_img_str = request.files["image"].read() 
        
        #Convert string data to numpy array
        uploaded_img_np = numpy.fromstring(uploaded_img_str, numpy.uint8)

        #Convert numpy array to image
        uploaded_img_cv = cv2.imdecode(uploaded_img_np, cv2.IMREAD_COLOR)

        try:
            decoded_object = pyzbar.decode(uploaded_img_cv) #type(decoded_object): list
        except:
            return apology("Could not decode barcode.")

        #Replace the originally uploaded image with one with a drawn rectangle around the barcode
        modified_img_b64 = modify(uploaded_img_cv, decoded_object)

        #Using url/api for barcode database, search for this barcode; the site name is https://www.upcitemdb.com/
        barcode = str(decoded_object[0].data)[2:-1]

        try:
            #Obtain product information and create a dictionary to store it
            barcode_url = "https://www.upcitemdb.com/upc/{}".format(barcode)
            page = requests.get("https://api.upcitemdb.com/prod/trial/lookup?upc={}".format(barcode))
            #print(page) --> if 200, all good. if start w 4/5, error.
            dump = json.loads(page.content)
            product_info = dump["items"][0]
        except:
            return apology("Barcode does not exist in database.")

        #If one of the pieces of information isn't available, return "N/A"
        for key, value in product_info.items():
            if value == '':
                product_info[key] = "N/A"

        #Check if vegan
        vegan_check = vegan_check(product_info["description"].upper().strip("INGREDIENTS:"))
        vegan_status = vegan_check[0] #"Yes" or "No"
        reason = vegan_check[1] #If "No", reason = the offending ingredient; if "Yes", reason = Null

        #Update barcode lookup history table
        now = datetime.now().strftime('%m-%d-%Y %H:%M')
        db.execute("INSERT INTO lookups(user_id, barcode, brand, title, vegan_status, barcode_url, time) VALUES (:user, :barcode, :brand, :title, :vegan_status, :barcode_url, :time)", 
            user=session["user_id"], barcode=barcode, brand=product_info["brand"], title=product_info["title"], vegan_status=vegan_status, barcode_url=barcode_url, time=now)
        
        flash("Barcode successfully looked up!")

        return render_template("barcodeinfo.html", product_info=product_info, vegan_status=vegan_status, reason=reason, modified_img=modified_img_b64)

    return apology("Sorry, something went wrong :(")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    #try:
    rows = db.execute("SELECT * FROM lookups WHERE user_id = :user", user=session["user_id"])
    lookups = []
    # Create a list with info about lookup, append to a list of every barcode lookup
    for row in rows:
        lookups.insert(0,list((row['brand'], row['title'], row['vegan_status'], row['barcode'], row['barcode_url'], row['time'])))
        

    return render_template("history.html", lookups=lookups)

    #except:
    #    return apology("sorry, something went wrong")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        session["username"] = request.form.get("username")

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("register.html")

    else:
        # Get username from form
        username = request.form.get("username")

        #Check that username is not blank and not already taken
        if not username:
            return apology("Your username cannot be blank.")
        if len(db.execute("SELECT 1 FROM users WHERE username=?", username)) != 0:
            return apology("Sorry, that username is taken.")
        
        #Get password & confirmation from form, & generate hash
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)

        #Check that password is not blank and that it matches the confirmation
        if not password:
            return apology("Your password cannot be blank.")
        elif not confirmation:
            return apology("You must enter your password a second time.")
        elif password != confirmation:
            return apology("Your passwords must match.")

        #Update database
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=username, hash=hash)

        #Redirect user to index
        return redirect("/")

    return apology("sorry, something went wrong")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
