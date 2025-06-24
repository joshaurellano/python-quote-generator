from typing import Union
from fastapi import FastAPI
import requests
import json
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()

api_key = os.getenv("API_KEY")

@app.get('/')
async def read_root():
    return {"Hello": "World"}

@app.get('/quote')
async def read_quote():

    return {"Quote": "Here is your quote"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q":q}

@app.post('/quote')
async def generatequote():
    url="https://openrouter.ai/api/v1/chat/completions"
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data={
        "model":"anthropic/claude-3-haiku",
        "messages":[
            {
            "role":"user",
            "content":"Give me motivational quote to uplift my mood and respond with the quote and the meaning only"
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    
    return response_data['choices'][0]['message']['content']
    # return response_data['id']