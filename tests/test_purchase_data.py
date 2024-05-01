from fastapi.testclient import TestClient
from src.main import app 
import json

client = TestClient(app)

API_KEY = "aebacdbb-86d4-4fdc-aa9f-63ed5aa0cfb7"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def test_add_and_get_purchase_history():
    with open('tests/test_data/Tesco-Customer-Data.json', 'r') as file:
        test_data = json.load(file)
    
    response = client.post("/add_purchase_history", headers=headers, json=test_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Purchase history added successfully"}

    response = client.get("/purchase_history", headers=headers)
    assert response.status_code == 200

    assert len(list(response.json().keys())) == 4