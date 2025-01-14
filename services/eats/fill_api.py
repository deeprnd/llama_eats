import json
import random
import uuid

def generate_food_description(dish_info):
    cooking_methods = ["Grilled", "Baked", "Fried", "Sautéed", "Roasted", "Slow-cooked", "Charred", "Steamed"]
    adjectives = ["Delicious", "Savory", "Hearty", "Mouthwatering", "Aromatic", "Flavorful", "Indulgent", "Exquisite"]

    # Randomly select ingredients
    random_ingredients = random.sample(dish_info['ingredients'], min(len(dish_info['ingredients']), 2))
    single_ingredient = random.choice(dish_info['ingredients'])

    # Generate ingredient phrases dynamically
    ingredient_phrases = [
        f"featuring {', '.join(random_ingredients)}",
        f"highlighting the rich flavors of {random_ingredients[0]} and {random_ingredients[1]}" if len(random_ingredients) > 1 else f"highlighting the rich flavor of {single_ingredient}",
        f"crafted with a touch of {single_ingredient}",
        f"elevated with {single_ingredient}",
    ]

    cooking_method = random.choice(cooking_methods)
    adjective = random.choice(adjectives)
    ingredient_phrase = random.choice(ingredient_phrases)

    return f"{adjective} {cooking_method} {dish_info['name']}, {ingredient_phrase}, served to perfection."

def generate_restaurant_name():
    adjectives = ["Cozy", "Spicy", "Golden", "Delicious", "Rustic", "Elegant", "Savory", "Tasty", "Vibrant", "Lush"]
    cuisines = ["Italian", "Mexican", "Thai", "Chinese", "French", "Japanese", "Mediterranean", "Indian", "Korean", "American"]
    themes = ["Grill", "Bistro", "Cafe", "Kitchen", "Diner", "Tavern", "House", "Bar", "Eatery", "Oven"]

    adjective = random.choice(adjectives)
    cuisine = random.choice(cuisines)
    theme = random.choice(themes)

    return f"{adjective} {cuisine} {theme}"

categories_with_dishes_ingredients = {
    "pizza": [
        {"name": "Margherita Pizza", "ingredients": ["basil", "mozzarella cheese", "tomato sauce", "olive oil", "salt"]},
        {"name": "Pepperoni Pizza", "ingredients": ["pepperoni", "mozzarella cheese", "tomato sauce", "olive oil", "oregano"]},
        {"name": "BBQ Chicken Pizza", "ingredients": ["chicken", "BBQ sauce", "red onions", "cilantro", "mozzarella cheese"]},
        {"name": "Veggie Pizza", "ingredients": ["bell peppers", "onions", "mushrooms", "black olives", "mozzarella cheese"]},
        {"name": "Hawaiian Pizza", "ingredients": ["ham", "pineapple", "mozzarella cheese", "tomato sauce", "olive oil"]},
        {"name": "Four Cheese Pizza", "ingredients": ["mozzarella cheese", "gorgonzola cheese", "parmesan cheese", "ricotta cheese", "olive oil"]},
        {"name": "Buffalo Chicken Pizza", "ingredients": ["buffalo sauce", "chicken", "blue cheese dressing", "celery", "mozzarella cheese"]},
        {"name": "Spinach & Feta Pizza", "ingredients": ["spinach", "feta cheese", "mozzarella cheese", "olive oil", "garlic"]},
        {"name": "Meat Lovers Pizza", "ingredients": ["pepperoni", "sausage", "bacon", "ham", "mozzarella cheese"]},
        {"name": "Pesto Chicken Pizza", "ingredients": ["pesto sauce", "chicken breast", "mozzarella cheese", "pine nuts", "arugula"]},
        {"name": "Sausage & Kale Pizza", "ingredients": ["Italian sausage","kale leaves","mozzarella cheese","tomato sauce","olive oil"]},
        {"name": "Garlic Prawn Pizza","ingredients":["prawns","garlic","mozzarella cheese","tomato sauce","parsley"]},
        {"name": "Deep Dish Sausage Pizza","ingredients":["sausage","mozzarella cheese","tomato sauce","bell peppers","onions"]},
        {"name": "Capricciosa","ingredients":["artichokes","ham","mushrooms","olives","mozzarella cheese"]},
        {"name": "Roast Cauliflower Cheese Pizza","ingredients":["cauliflower","cheddar cheese","mozzarella cheese","olive oil","thyme"]},
        {"name": "Spinach & Blue Cheese Pizza","ingredients":["spinach","blue cheese","mozzarella cheese","walnuts","olive oil"]},
        {"name": "Prosciutto & Rocket Pizza","ingredients":["prosciutto","rocket leaves","parmesan cheese","mozzarella cheese","balsamic glaze"]},
        {"name": "BBQ Meatlovers Pizza","ingredients":["beef brisket","pulled pork","BBQ sauce","onions","cheddar cheese"]},
        {"name": "Potato & Rosemary Pizza","ingredients":["potatoes","rosemary","mozzarella cheese","olive oil","sea salt"]},
        {"name": "Rainbow Pizza","ingredients":["bell peppers of various colors","mozzarella cheese","tomato sauce","onions","black olives"]}
    ],
    "burger": [
        {"name": "Cheeseburger", "ingredients": ["beef patty", "cheddar cheese", "lettuce", "tomato", "pickles"]},
        {"name": "Veggie Burger", "ingredients": ["black beans", "quinoa", "avocado", "lettuce", "tomato"]},
        {"name": "Bacon Burger", "ingredients": ["beef patty", "bacon", "cheddar cheese", "lettuce", "BBQ sauce"]},
        {"name": "Mushroom Swiss Burger", "ingredients": ["beef patty", "mushrooms", "swiss cheese", "garlic aioli", "lettuce"]},
        {"name": "BBQ Bacon Burger", "ingredients": ["beef patty", "BBQ sauce", "bacon", "onion rings", "cheddar cheese"]},
        {"name": "Spicy Jalapeño Burger", "ingredients": ["beef patty", "jalapeños", "pepper jack cheese", "sriracha mayo", "lettuce"]},
        {"name": "Blue Cheese Burger", "ingredients": ["beef patty", "blue cheese crumbles", "caramelized onions", "arugula", "balsamic glaze"]},
        {"name": "Turkey Burger", "ingredients": ["turkey patty", "avocado", "lettuce", "tomato", "chipotle mayo"]},
        {"name": "Black Bean Burger", "ingredients": ["black beans","quinoa","corn","cilantro","avocado"]},
        {"name": "Lamb Burger with Tzatziki", "ingredients": ["lamb patty","tzatziki sauce","cucumber","red onion","feta"]},
        {"name": "Pineapple Teriyaki Burger","ingredients":["beef patty","teriyaki sauce","pineapple slice","lettuce","sesame seed bun"]},
        {"name": "Avocado Burger","ingredients":["beef patty","avocado","pepper jack cheese","lettuce","tomato"]},
        {"name": "Fried Egg Burger","ingredients":["beef patty","fried egg","bacon","cheddar cheese","lettuce"]},
        {"name": "Sliders with Assorted Toppings","ingredients":["mini beef patties","various cheeses","pickles","lettuce","special sauce"]},
        {"name": "Greek Lamb Burger","ingredients":["lamb patty","feta cheese","tzatziki sauce","red onion","cucumber"]},
        {"name": "Crispy Chickpea Burger","ingredients":["chickpeas","spices","avocado","lettuce","tahini sauce"]},
        {"name": "Chipotle Chicken Burger","ingredients":["grilled chicken breast","chipotle mayo","lettuce","tomato","onions"]},
        {"name": "Buffalo Cauliflower Burger","ingredients":["breaded cauliflower patty","buffalo sauce","blue cheese dressing","lettuce","pickle"]},
        {"name": "Classic American Burger","ingredients":["beef patty","American cheese","ketchup","mustard","pickles"]}, 
    ],
    "sushi": [
        {"name": "California Roll","ingredients":["crab meat or imitation crab, avocado, cucumber, rice, nori seaweed"]}, 
		{"name": "Spicy Tuna Roll","ingredients":["tuna, spicy mayo, cucumber, rice, nori seaweed"]}, 
		{"name": "Salmon Sashimi","ingredients":["salmon, wasabi, soy sauce, pickled ginger, sesame seeds"]}, 
		{"name": "Tempura Roll","ingredients":["shrimp tempura, avocado, cucumber, rice, nori seaweed"]}, 
		{"name": "Dragon Roll","ingredients":["eel, avocado, cucumber, rice, eel sauce"]}, 
		{"name": "Rainbow Roll","ingredients":["variety of fish (tuna, salmon), avocado, cucumber, rice, nori seaweed"]}, 
		{"name": "Philadelphia Roll","ingredients":["smoked salmon, cream cheese, cucumber, rice, nori seaweed"]}, 
		{"name": "Eel Avocado Roll","ingredients":["eel, avocado, rice, nori seaweed, eel sauce"]}, 
		{"name": "Shrimp Tempura Roll","ingredients":["shrimp tempura, avocado, rice, nori seaweed, spicy mayo"]}, 
		{"name": "Vegetable Roll","ingredients":["cucumber, avocado, carrot, rice, nori seaweed"]}, 
		{"name": "Crab Rangoon Roll","ingredients":["crab meat or imitation crab, cream cheese, green onions, rice, nori seaweed"]}, 
		{"name": "Tuna Tataki","ingredients":["tuna steak, soy sauce, sesame seeds, green onions, wasabi"]}, 
		{"name": "Miso Soup with Tofu","ingredients":["miso paste, tofu cubes, green onions, seaweed flakes (wakame), dashi broth"]}, 
		{"name": "Sushi Burrito","ingredients":["sushi rice, assorted fillings (fish/veggies), nori seaweed wrap"]}, 
		{"name": "Sashimi Platter","ingredients":["assorted fish slices (salmon,tuna), wasabi,sliced lemon,sesame seeds,sliced radish"]}, 
        {"name": "Inari Sushi","ingredients":["sweet tofu pouches (inari), sushi rice,sesame seeds,cucumber strips,nori strips"]}, 
        {"name": "Nigiri Sushi","ingredients":["sushi rice,fresh fish slice (salmon,tuna),wasabi,nori strip,sesame seeds"]}, 
        {"name": "Cucumber Roll","ingredients":["cucumber,sushi rice,nori seaweed,sesame seeds,dipping soy sauce"]}, 
        {"name": "Spicy Salmon Roll","ingredients":["salmon,tobiko (fish roe),spicy mayo,cucumber,nori seaweed"]},  
        {"name": "Pork Katsu Sushi","ingredients":["pork loin cutlet,panko breadcrumbs,rice,nori seaweed,tonkatsu sauce"]}
    ],
    "italian": [
        {"name": "Spaghetti Carbonara", "ingredients": ["spaghetti", "eggs", "parmesan cheese", "guanciale", "black pepper"]},
        {"name": "Lasagna", "ingredients": ["lasagna noodles", "ricotta cheese", "mozzarella cheese", "ground beef", "tomato sauce"]},
        {"name": "Pesto Genovese", "ingredients": ["basil", "pine nuts", "garlic", "parmesan cheese", "olive oil"]},
        {"name": "Risotto alla Milanese", "ingredients": ["arborio rice", "saffron", "onion", "white wine", "parmesan cheese"]},
        {"name": "Margherita Pizza", "ingredients": ["pizza dough", "tomato sauce", "mozzarella cheese", "fresh basil", "olive oil"]},
        {"name": "Gnocchi al Pesto", "ingredients": ["gnocchi", "pesto sauce", "parmesan cheese", "pine nuts", "olive oil"]},
        {"name": "Osso Buco alla Milanese", "ingredients": ["veal shanks", "white wine", "carrots", "celery", "onions"]},
        {"name": "Fettuccine Alfredo", "ingredients": ["fettuccine pasta", "butter", "heavy cream", "parmesan cheese", "black pepper"]},
        {"name": "Eggplant Parmesan (Melanzane alla Parmigiana)", "ingredients": ["eggplant", "tomato sauce", "mozzarella cheese", "parmesan cheese", "basil"]},
        {"name": "Bruschetta al Pomodoro", "ingredients": ["ciabatta bread", "tomatoes", "garlic", "basil", "olive oil"]},
        {"name": "Cacio e Pepe", "ingredients": ["spaghetti", "pecorino romano cheese", "black pepper", "salt", "pasta water"]},
        {"name": "Tiramisu", "ingredients": ["ladyfingers", "mascarpone cheese", "espresso", "cocoa powder", "sugar"]},
        {"name": "Caprese Salad","ingredients":["fresh mozzarella","tomatoes","basil","olive oil","balsamic vinegar"]}, 
        {"name": "Fritto Misto","ingredients":["shrimp","calamari","zucchini","flour","lemon"]}, 
        {"name": "Polenta con Salsicce","ingredients":["polenta","Italian sausage","onions","garlic","parmesan cheese"]}, 
        {"name": "Pappa al Pomodoro","ingredients":["stale bread","ripe tomatoes","garlic","basil","olive oil"]}, 
        {"name": "Arancini","ingredients":["risotto rice","mozzarella cheese","peas","breadcrumbs","marinara sauce"]}, 
        {"name": "Trofie al Pesto Genovese","ingredients":["trofie pasta","basil pesto","green beans","potatoes","parmesan cheese"]}, 
        {"name": "Saltimbocca alla Romana","ingredients":["veal cutlets","prosciutto","sage leaves","white wine","butter"]}, 
        {"name": "Cannoli","ingredients":["cannoli shells","ricotta cheese","powdered sugar","chocolate chips","vanilla extract"]}
    ]
}

def generate_random_venue(i):
    days_of_week = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    num_days = random.randint(1, len(days_of_week))
    selected_days = random.sample(days_of_week, num_days)

    service_availability = []
    for day in selected_days:
        start_hour = random.randint(8, 12)
        end_hour = random.randint(start_hour + 1, 23)
        service_availability.append({
            "day_of_week": day,
            "time_periods": [{
                "start_time": f"{start_hour:02d}:00",
                "end_time": f"{end_hour:02d}:00"
            }]
        })

    venue = {
        "store_id": str(uuid.uuid4()),
        "name": generate_restaurant_name(),
        "address": f"{random.randint(1, 1000)} Main St., City{random.randint(1, 10)}",
        "category_ids": random.sample(list(categories_with_dishes_ingredients.keys()), k=random.randint(1, 3)),
        "proximity": round(random.uniform(0.1, 10.0), 2),
        "service_availability": service_availability
    }
    return venue

if __name__ == "__main__":
    venues = []
    for i in range(1, 101):
        venue = generate_random_venue(i)
        venues.append(venue)

    with open("venues.json","w") as file:
        json.dump(venues,file ,indent=2)

    menus = {}
    for venue in venues:
        store_id = venue["store_id"]
        menu_items = []
        for category in venue["category_ids"]:
            dishes = random.sample(range(1, len(categories_with_dishes_ingredients[category])), random.randint(1, len(categories_with_dishes_ingredients[category]) - 1))

            for i in dishes:
                dish_info = categories_with_dishes_ingredients[category][i]
                item = {
                    "id" : str(uuid.uuid4()),
                    "title" : dish_info["name"],
                    "subtitle" : generate_food_description(dish_info),
                    "ingredients": dish_info["ingredients"],
                    "price" : round(random.uniform(5.99 ,29.99),2),
                    "category": category
                }
            menu_items.append(item)
            menus[store_id] = menu_items

    # Save menus data to menus.json
    with open("menus.json","w") as file:
        json.dump(menus,file ,indent=2)