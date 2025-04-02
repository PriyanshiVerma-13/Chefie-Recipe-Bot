import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

def get_recipe_details(user_query):
    """Fetch recipe based on user input (both by ingredients & keyword search)"""
    
    # Try searching by ingredients first
    ingredients = user_query.split()  # Split user input into words
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={','.join(ingredients)}&number=5&apiKey={API_KEY}"
    response = requests.get(url).json()

    if not response or isinstance(response, dict):  # If no result, try a keyword search
        url = f"https://api.spoonacular.com/recipes/complexSearch?query={user_query}&number=5&apiKey={API_KEY}"
        response = requests.get(url).json().get("results", [])

    if response:  
        # Find the best-matching recipe
        best_match = response[0]  # Default to first result
        for recipe in response:
            if any(word.lower() in recipe["title"].lower() for word in ingredients):
                best_match = recipe
                break

        recipe_id = best_match["id"]

        # Fetch full recipe details
        details_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={API_KEY}"
        details = requests.get(details_url).json()

        return {
            "title": details["title"],
            "ingredients": [ing["name"] for ing in details.get("extendedIngredients", [])],
            "steps": [step["step"] for step in details.get("analyzedInstructions", [{}])[0].get("steps", [])]
        }

    return {"error": "No recipe found for your request. Try different keywords!"}



def get_substitutions(ingredient):
    """Fetch alternative ingredient suggestions"""
    url = f"https://api.spoonacular.com/food/ingredients/substitutes?ingredientName={ingredient}&apiKey={API_KEY}"
    response = requests.get(url).json()
    
    return response.get("substitutes", ["No substitutes found"])

def check_allergens(ingredients):
    """Check if any ingredients contain allergens."""
    found_allergens = [item for item in ingredients if item.lower() in allergens]
    if found_allergens:
        return f"⚠️ Warning! This recipe contains: {', '.join(found_allergens)}."
    return "✅ This recipe does not contain common allergens."
