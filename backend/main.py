from fastapi import FastAPI, WebSocket
import json
from nlp_utils import extract_intent_and_entities, explain_cooking_term
from recipe_utils import get_recipe_details, get_substitutions, check_allergens

app = FastAPI()
user_sessions = {}

def format_recipe(recipe):
    """Format the recipe for better readability."""
    return f"\n🍽️ **{recipe['title']}**\n\n🥕 **Ingredients:**\n- " + "\n- ".join(recipe["ingredients"]) + "\n\n👨‍🍳 **Steps:**\n" + "\n".join(f"{i+1}. {step}" for i, step in enumerate(recipe["steps"]))

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    user_id = str(websocket.headers.get("sec-websocket-key", websocket.client))

    if user_id not in user_sessions:
        user_sessions[user_id] = {"history": [], "last_recipe": None, "allergens": None, "diet": None}

    print("WebSocket Connected ✅")

    await websocket.send_text("Hello! Do you have any dietary preferences? (Veg/Non-Veg)")
    diet_preference = await websocket.receive_text()
    user_sessions[user_id]["diet"] = diet_preference.lower()

    await websocket.send_text("Do you have any allergens I should consider? (e.g., peanuts, dairy, none)")
    allergens = await websocket.receive_text()
    user_sessions[user_id]["allergens"] = allergens.lower()
    
    await websocket.send_text("Great! Now, tell me what you need help with.")
    
    while True:
        try:
            data = await websocket.receive_text()
            print(f"User: {data}")

            # NLP-based intent detection
            intent, entities = extract_intent_and_entities(data)

            if intent == "substitution":
                ingredient = entities[-1] if entities else None
                bot_reply = f"You can use: {', '.join(get_substitutions(ingredient))}" if ingredient else "What ingredient do you want to replace?"
            
            elif intent == "cooking_explanation":
                term = entities[0] if entities else None
                bot_reply = explain_cooking_term(term) if term else "What cooking term do you want to know about?"
            
            elif intent == "allergen_check":
                user_allergens = user_sessions[user_id]["allergens"].split(", ") if user_sessions[user_id]["allergens"] else []
                allergens_found = check_allergens(entities, user_allergens)
                bot_reply = allergens_found if entities else "Which ingredient do you want me to check?"

            else:  # Default to fetching a recipe
                try:
                    parsed_data = json.loads(data)
                    ingredients = ", ".join(parsed_data) if isinstance(parsed_data, list) else data.strip()
                except json.JSONDecodeError:
                    ingredients = data.strip()

                if not ingredients:
                    bot_reply = "Please provide at least one ingredient."
                else:
                    if user_sessions[user_id]["diet"] == "veg":
                        recipe = get_recipe_details(user_query=ingredients, diet="veg")
                    else:
                        recipe = get_recipe_details(ingredients)

                    user_sessions[user_id]["last_recipe"] = recipe

                    if "error" in recipe:
                        bot_reply = recipe["error"]
                    else:
                        # Filter out allergens
                        user_allergens = user_sessions[user_id]["allergens"].split(", ") if user_sessions[user_id]["allergens"] else []
                        filtered_ingredients = [ing for ing in recipe["ingredients"] if not any(allergen in ing.lower() for allergen in user_allergens)]
                        recipe["ingredients"] = filtered_ingredients
                        bot_reply = format_recipe(recipe)

            user_sessions[user_id]["history"].append(bot_reply)
            await websocket.send_text(bot_reply)

        except Exception as e:
            print(f"WebSocket Error: {e}")
            await websocket.close()
