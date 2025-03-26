import requests 
from fastapi import FastAPI, WebSocket
import json
import os
from dotenv import load_dotenv

load_dotenv()

app=FastAPI()

API_KEY= os.getenv("SPOONACULAR_API_KEY")

def search_recipes(ingredients):
    url=f"https://api.spoonacular.com/recipes/findByIngredients?ingredients={','.join(ingredients)}&number=5&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        ingredients = data.split(",")
        recipes = search_recipes(ingredients)
        if recipes:
            await websocket.send_text(json.dumps(recipes))
        else:
            await websocket.send_text(json.dumps({"error":"ccould not find recipes"}))
