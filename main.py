from typing import Union
from fastapi import FastAPI
import requests
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
load_dotenv()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")

@app.get('/')
async def read_root():
    return {"Hello": "World"}

@app.get('/quote')
async def read_quote():
    response = requests.get(api_url)

    if response.status_code == requests.codes.ok:
        print(response.text)
        parsedResponse = json.loads(response.text)
        quote = parsedResponse[0]['content']
        author = parsedResponse[0]['author']
        return parsedResponse
    else:
        print("Error:", response.status_code, response.text)

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
            "content":"Give me motivational quote to uplift my mood"
            }
        ]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_data = response.json()
    
    return response_data['choices'][0]['message']['content']
    # return response_data['id']