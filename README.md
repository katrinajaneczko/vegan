# Is It Vegan? Web App
For my final project, I decided to make Is It Vegan?. I used Flask, JavaScript, HTML, CSS, OpenCV, and SQLite to do so.
This web app was built to make the endeavor of checking whether a food product is vegan or not a bit easier. 
A user takes a photo of the barcode of the food product in question and uploads it to the site. 
Then, using a barcode database, the program runs and shows the user some info about the product and concludes whether its ingredients are vegan or not.
It also displays a modified version of the original image but with a green rectangle around the barcode.
The Look Up page lets you upload and look up a barcode. 
Under History is a log of the user's past lookups.
Index is an explanation of the web app, how it works, and why it's important.
The About Veganism page provides information about veganism and external resources such as recipe blogs and documentaries.

# Video
Click this link for the video walkthrough: https://youtu.be/RsRYtVAmywg 

# Video Transcript
Hi, my name is Katrina Janeczko and I am a sophomore at Temple University. 
In this video I'm going to walk you through my final project for my first ever compsci course, CIS 1051, or Intro to Problem Solving and Programming in Python. 
First I’m just gonna register, login, and show you how it works while I give you a little bit of a backstory.
So I went vegan a couple years ago, and if you don’t know, it’s basically a diet free from animal products. 
By now, I’m pretty well versed in quickly scanning through an ingredients list and being able to decipher whether a food product is vegan or not. 
But it can be annoying and tricky when the ingredients lists are super long and are printed really tiny and squished on a package. 
And so with my web app, you can actually upload a picture either here or here if you click Look Up, and it’ll tell you actually whether it's vegan or not. 
Here I’ve got a couple sample images I’d already taken. This one is of bagels, and we're gonna find out whether they are vegan or not based on the barcode.
As you can see here, they are vegan. It'll also give you the brand, product name, the barcode, the ingredients list,
and it’ll also spit back the picture you gave it but with a green rectangle around the barcode. 
Next up we’ll try Hot Pockets. Spoiler alert, they are not vegan.
They've got ham, cheese, and a whole bunch of offending ingrdients in them.
As you can see, it'll tell you the reason it's not vegan it because of the ham. That's because the program will identify the first offending ingredient.
Now if I go over to the History page, I can see all my past lookups, 
and clicking this link over here that's green will take me to the barcode database website where I got the information. 
And clicking About Veganism brings me to some info and resources about the diet. 
And I know what what you're thinking, "I'm not gonna carry my PC around Giant and 7-11, how the heck am I gonna use this?!" 
and don't you worry cause there is a mobile version.
A couple things gave me the idea for this project, one of them being when my mom came home from the grocery store complaining how difficult it was to tell whether this bread was vegan cause it’s so hard to read and she wasnt really sure whether certain ingredients were vegan. 
Like, what the heck is monodiglycerides anyway, she shouldn’t have to google that to buy me bread.
After taking this class, my biggest takeaway is: why do something by hand when you can automate it and make life easier?
And so boom, there you have it, snap a picture and find out if it’s vegan in a matter of seconds.
And all it took was hours and hours and hours of my blood, sweat, and tears to learn Flask, HTML, cCSS, OpenCV, and SQLite,
and some more things like how to use VSCode and how to read things on StackExchange.
No but, in all seriousness, this project is very important to me. It certainly isn’t finished, but I don't remember the last time I was this proud of myself. 
And I can’t wait to make it better. Thank you to Professor Rosen and my TA Tamara for helping me on this learning journey.

# How It's Organized
I used the Flask Python web app framework, and so app.py is where everything is basically run from. 
It has all the routes, which include functions which run some Python code and/or open one of the HTML pages from the /templates folder.
The templates all extend layout.html so they all have a horizontal nav bar and the same look.
There is an ability to register for an account and login, for which I used SQLite as the database. 
I make sure the password is hashed before storing it and usernames cannot be repeated.
The page apology.html corresponds with the apology function which renders an apology message custom to the problem when something goes wrong 
(like if the barcode cannot be read or doesn't exist in the database).
The homepage (index.html) and about.html are mostly text, while barcodeinfo.html, login.html, and register.html include forms. 
Then barcodeinfo.html shows text and an image thanks to Django, using {% %} to insert variables from app.py, and history.html is a table created in a similar fashion.
/static contains the css stylesheet, the icon (image), and text files like the list of nonvegan ingredients or the exceptions.
barcodes.db has the database info in it, which I open with DB Broswer for SQLite.
helpers.py are juust some helper functions (I got the idea from the CS50 course from their Finance project).

# What I Did
I used the web track from the CS50 course at https://cs50.harvard.edu/x/2020/tracks/web/ to learn a lot of what I needed to know, and I used their /finance project as a basis for which to make my own web app.
I made the program using OpenCV documentation here https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_intro/py_intro.html.
I used Bootstrap and CSS to make my site look nice. https://getbootstrap.com/docs/3.4/css/
W3Schools https://www.w3schools.com/ was super helpful in my learning as well. 
I first made a Python program that would us cv2 to take an image file of a food product's barcode and find its barcode number, then use https://www.upcitemdb.com/ to look up its ingredients and print them out.
Then I wrote a program to check whether ingredients in a list were vegan or not. I put it all together in Flask Python web app framework.
Oh, and I also made the little carrot logo with Google Drawings!

# How It Works
When a user uploads an image to the form on barcodeupload.html, it is first retrieved and read into string data, 
which is converted to a numpy array.
Using cv2, this is converted to a an image that OpenCV can read and decode. 
The modify() function takes the uploaded image and decoded object and finds the points of the rectangle formed by the barcode, 
returning the original image modified to have a green rectangle around the barcode, but not before being converted to base64 as a string.
That is what is embedded in the barcodeinfo.html page when the image is displayed.
Next, the barcode upc digits are found by splicing the decoded object data and that is inserted as a variable into a url that
uses https://www.upcitemdb.com/ to look up info about the product whose barcode it is.
It returns a json file that includes info like brand, product title, and ingredients, which are extracted and stored as variables.
If one of those dictionary keys doesn't exist in the original json, then "N/A" replaces it as the value in my program so it isn't blank.
Now, the function vegan_check() will do some file reading. 
It turns the not_vegan_list.txt, which is a list of nonvegan ingredients, into a list called nonvegan, as well as vegan_exceptions.txt into a list called exceptions.
Lots of stripping and replacing is involved in this next step, wherein the ingredients that come from the json file
are read into a list called ingredients.
Then, a nexted for loop with an if statement checks for each ingredient in ingredients, for each item in nonvegan,
if the string for item is in the string for ingredient, and the string "vegan" is not in the ingredient (to account for an ingredient like "vegan chicken")
and the string for ingredient is not in the exceptions list (to account for items like "almond milk"),
then the function returns a list of 2 things: a string "No" and the offending ingredient.
If that isn't the case, it returns "Yes" and None.
Then, the time will be captured so that the History table can be updated,
and the user sees the page barcodeinfo.html with the ifnormation in question, including 
whether or not the product is vegan.

# Challenges
Since this is my first ever CIS course, not just at Temple, but anywhere, I had a lot of learning to do in order to accomplish this project.
Flask, HTML, CSS, OpenCV, and SQLite were completely foreign to me upon beginning this project.
That was definitely my biggest challenge. Oftentimes, I felt so frustrated that I wanted to give up. 
But with hours and hours of work, patience, and googling, I managed to come up with something that works!

# What Still Has To Be Done
I would like to make the site look better. I want to add images and work on the design.
I also would like to add to my program the ability to distinguish between a QR code and barcode and then ignore the QR code.
Right now it doesn't do that, and instead throws an error because it think's it's reading 2 barcodes.
Maybe my next project will be trying to turn it into an Android application.

# What I Learned
I learned so much about web development and design, from Flask and JS to HTML and CSS. 
I learned about patience in debugging. 
I learned how to sift through stuff on Stack Exchange and how to use a terminal and pip3 and VSCode.
I learned how when you've been working at a program for hours and days and weeks and you finally have everything together,
and you've debugged everything, and it finally works the way you want it to, it's the best feeling in the world.
I also learned that even after so much work, a project like this is never really finished. Every time I think I'm done, I find more things to do to improve it.
I learned that I really like this and I want to continue with CIS classes. 
I started the year with a declared major in Environmental Science and am ending it with one in Mathematics & Computer Science.
Basically, I learned that I want to keep learning.

# Thank You
Thank you to Professor Rosen and my TA, Tamara, for being so amazing, helpful, and encouraging.
