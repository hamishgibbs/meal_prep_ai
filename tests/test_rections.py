from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from src.main import app 
import json
from datetime import datetime

client = TestClient(app)

API_KEY = "aebacdbb-86d4-4fdc-aa9f-63ed5aa0cfb7"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def test_add_recipe_reaction():
    # Ensure the file is empty/clean before the test
    with open('recipes.json', 'w') as file:
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

    reaction = {
        "timestamp": datetime.strptime("2021-01-01", "%Y-%m-%d"),
        "text": "like"
    }

    reaction_dict = jsonable_encoder(reaction)

    response = client.post("/add_recipe_reaction/Test Recipe", headers=headers, json=reaction_dict)
    assert response.status_code == 200
    assert response.json() == {"message": "Reaction added successfully"}

    response = client.get("/recipes", headers=headers)
    assert response.status_code == 200
    assert response.json() == [{"name": "Test Recipe", "urls": ["http://example.com/"], "ingredients": [{"name": "Sugar", "quantity": "2 cups"}], "reactions": [reaction_dict]}]



