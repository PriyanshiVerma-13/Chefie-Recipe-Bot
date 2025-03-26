import requests
from fastapi import FastAPI, WebSocket
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("SPOONACULAR_API_KEY")

def search_recipes(ingredients):
    url = f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={','.join(ingredients)}&number=5&apiKey={API_KEY}"
    print(f"API URL: {url}")  # Debugging
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "API request failed"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket Connection Established ✅")  # Debugging

    while True:
        try:
            data = await websocket.receive_text()
            print(f"Received from Client: {data}")  # Debugging

            ingredients = data.split(",")  # Convert user input into a list
            recipes = search_recipes(ingredients)

            await websocket.send_text(json.dumps(recipes))
        except Exception as e:
            print(f"WebSocket Error: {e}")
            await websocket.close()
