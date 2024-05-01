from fastapi.testclient import TestClient
from src.main import app 
import json
import os

client = TestClient(app)

API_KEY = "aebacdbb-86d4-4fdc-aa9f-63ed5aa0cfb7"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def test_add_recipes():
    with open('data/recipes.json', 'w') as file:
        json.dump([], file)

    recipe1 = {
        "name": "Test Recipe",
        "urls": ["http://example.com/"],
        "ingredients": [{"name": "Sugar", "quantity": "2 cups"}],
        "reactions": []
    }

    recipe2 = {
        "name": "Test Recipe 2",
        "urls": ["http://example.com/"],
        "ingredients": [{"name": "Sugar", "quantity": "2 cups"}],
        "reactions": []
    }

    response = client.post("/add_recipe", headers=headers, json=recipe1)
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe 'Test Recipe' added successfully"}

    response = client.post("/add_recipe", headers=headers, json=recipe2)
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe 'Test Recipe 2' added successfully"}

    response = client.get("/recipe_names", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["Test Recipe", "Test Recipe 2"]

    response = client.get("/recipes", headers=headers)
    assert response.status_code == 200
    assert response.json() == [recipe1, recipe2]

def test_remove_recipe():
    with open('data/recipes.json', 'w') as file:
        json.dump([], file)

    recipe1 = {
        "name": "Test Recipe",
        "urls": ["http://example.com/"],
        "ingredients": [{"name": "Sugar", "quantity": "2 cups"}],
        "reactions": []
    }

    response = client.post("/add_recipe", headers=headers, json=recipe1)
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe 'Test Recipe' added successfully"}


    response = client.get("/recipe_names", headers=headers)
    assert response.status_code == 200
    assert response.json() == ["Test Recipe"]

    response = client.delete("/remove_recipe/Test Recipe", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Recipe 'Test Recipe' removed successfully"}




