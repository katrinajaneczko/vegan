
ing1 = "Water, Tomato Paste (paste, tomatoes, spices [parsley, salt]), Carrots, Celery, Light Red Kidney Beans, Potatoes, Green Beans, Dried Peas, Penne Rigate Pasta (semolina Wheat), Spinach, Garbanzo Beans. Contains Less Than 1% Of-Modified Corn Starch, Salt, Soybean Oil, Sugar, Potassium Chloride, Corn Protein (hydrolyzed), Tomato Extract, Spice, Dried Parsley, Maltodextrin, Natural Flavor, Citric Acid, Garlic Powder, Olive Oil, Turmeric Extract (color), Yeast Extract, Soy Lecithin, Nonfat Dried Milk."
ing2 = "Corn, Corn Oil, Honey Bbq Seasoning (salt, Maltodextrin [made From Corn], Sugar, Brown Sugar, Onion Powder, Monosodium Glutamate, Dextrose, Honey Solids, Spices, Tomato Powder, Molasses Solids, Yeast Extract, Artificial Color [yellow 5 Lake, Yellow 6 Lake, Blue 2 Lake, Red 40, Yellow 5, Blue 1], Natural And Artificial Flavors, Garlic Powder, Corn Starch, Citric Acid, Disodium Inosinate, And Disodium Guanylate)."

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

    #Tidy up the ingredients into a list, split into entries by commas
    ingredients = ingredients.replace(".", ",").replace("(" , ",").replace("[" , ",").replace(")" , "").replace("]" , "").split(",")

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
            if item in ingredient and ("vegan" not in ingredient or ingredient not in exceptions):
                reason = ingredient
                return ["No", reason]
    return ["Yes", None]

vegan_check = vegan_check(ing1.upper())
vegan_status = vegan_check[0] #"Yes" or "No"
reason = vegan_check[1] #If "No", reason = the offending ingredient; if "Yes", reason = Null

print(vegan_status, reason)