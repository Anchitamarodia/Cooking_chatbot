from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import openai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS setup for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI API key from .env file
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Database connection
DB_PATH = "./database/db.sqlite"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Pydantic model for user input
class UserInput(BaseModel):
    ingredients: list[str]
    dietary_preference: str  # vegetarian, vegan, non-veg
    region: str  # e.g., South Indian, North Indian

@app.get("/")
def health_check():
    return {"status": "API is running"}

@app.post("/get-recipe")
def suggest_recipe(user_input: UserInput):
    try:
        # Generate prompt for OpenAI GPT model based on user input
        prompt = (
            f"Suggest a {user_input.dietary_preference} recipe using ingredients: "
            f"{', '.join(user_input.ingredients)}. The recipe should be suitable for "
            f"{user_input.region} cuisine and require minimal cooking tools."
        )
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        
        recipe = response.choices[0].text.strip()
        return {"recipe": recipe}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
