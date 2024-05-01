from fastapi import FastAPI, HTTPException, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, HttpUrl, ValidationError
from typing import List, Optional
import json
from datetime import datetime

class Ingredient(BaseModel):
    name: str
    quantity: str

class Reaction(BaseModel):
    timestamp: str
    text: str

class Recipe(BaseModel):
    name: str
    urls: List[HttpUrl]
    ingredients: List[Ingredient]
    reactions: List[Reaction]

    @property
    def url_str(self):
        return [str(url) for url in self.urls]

    def model_dump(self):
        return {
            "name": self.name,
            "urls": self.url_str,
            "ingredients": [ingredient.model_dump() for ingredient in self.ingredients],
            "reactions": [reaction.model_dump() for reaction in self.reactions]
        }

class MealPlan(BaseModel):
    date: datetime
    recipes: List[str]
    shopping_list: List[str]

RECIPES_FILE = 'data/recipes.json'
MEAL_PLAN_FILE = 'data/meal_plan.json'

security = HTTPBearer()

def load_recipes():
    try:
        with open(RECIPES_FILE, 'r') as file:
            recipes = json.load(file)
        return recipes
    except FileNotFoundError:
        return []
    
def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    correct_token = "aebacdbb-86d4-4fdc-aa9f-63ed5aa0cfb7"
    if credentials.credentials != correct_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

app = FastAPI()

@app.post("/add_recipe")
async def add_recipe(recipe: Recipe, token: str = Depends(authenticate)):
    try:
        with open(RECIPES_FILE, 'r') as file:
            recipes = json.load(file)
    except FileNotFoundError:
        recipes = []

    if any(r['name'] == recipe.name for r in recipes):
        raise HTTPException(status_code=400, detail="Recipe already exists")

    recipes.append(recipe.model_dump())

    with open(RECIPES_FILE, 'w') as file:
        json.dump(recipes, file, indent=4)

    return {"message": f"Recipe '{recipe.name}' added successfully"}

@app.get("/recipe_names", response_model=List[str])
async def recipe_names(token: str = Depends(authenticate)):
    recipes = load_recipes()
    recipe_names = [recipe['name'] for recipe in recipes]
    return recipe_names

@app.get("/recipes")
async def recipes(token: str = Depends(authenticate)):
    recipes = load_recipes()
    return recipes

@app.delete("/remove_recipe/{recipe_name}")
async def remove_recipe(recipe_name: str, token: str = Depends(authenticate)):
    recipes = load_recipes()

    updated_recipes = [recipe for recipe in recipes if recipe['name'] != recipe_name]
    if len(recipes) == len(updated_recipes):
        raise HTTPException(status_code=404, detail="Recipe not found")

    with open(RECIPES_FILE, 'w') as file:
        json.dump(updated_recipes, file, indent=4)

    return {"message": f"Recipe '{recipe_name}' removed successfully"}

@app.post("/add_meal_plan")
async def add_meal_plan(meal_plan: MealPlan, token: str = Depends(authenticate)):
    try:
        with open(MEAL_PLAN_FILE, 'r') as file:
            existing_meal_plans = json.load(file)
    except FileNotFoundError:
        existing_meal_plans = []

    meal_plan_dict = jsonable_encoder(meal_plan)

    existing_meal_plans.append(meal_plan_dict)

    with open(MEAL_PLAN_FILE, 'w') as file:
        json.dump(existing_meal_plans, file, indent=4)

    return {"message": "Meal plan saved successfully"}

@app.get("/meal_plans")
async def get_meal_plans(token: str = Depends(authenticate)):
    try:
        with open(MEAL_PLAN_FILE, 'r') as file:
            meal_plans = json.load(file)
        return meal_plans
    except FileNotFoundError:
        return []

@app.post("/add_recipe_reaction/{recipe_name}")
async def add_recipe_reaction(recipe_name: str, reaction: Reaction, token: str = Depends(authenticate)):
    recipes = load_recipes()

    for recipe in recipes:
        if recipe['name'] == recipe_name:
            recipe['reactions'].append(reaction.dict())
            break
    else:
        raise HTTPException(status_code=404, detail="Recipe not found")

    with open(RECIPES_FILE, 'w') as file:
        json.dump(recipes, file, indent=4)

    return {"message": "Reaction added successfully"}