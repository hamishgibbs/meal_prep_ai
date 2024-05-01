from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
from src.main import app 
from datetime import datetime
import json

client = TestClient(app)

API_KEY = "aebacdbb-86d4-4fdc-aa9f-63ed5aa0cfb7"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def test_add_meal_plan():

    with open('meal_plan.json', 'w') as file:
        json.dump([], file)

    meal_plan = {
        "date": datetime.strptime("2021-01-01", "%Y-%m-%d"),
        "recipes": ["Test Recipe", "Test Recipe 2"],
        "shopping_list": ["Sugar"]
    }

    meal_plan_dict = jsonable_encoder(meal_plan)

    response = client.post("/add_meal_plan", headers=headers, json=meal_plan_dict)
    assert response.status_code == 200
    assert response.json() == {"message": "Meal plan saved successfully"}

    response = client.get("/meal_plans", headers=headers)
    assert response.status_code == 200
    assert response.json() == [meal_plan_dict]
