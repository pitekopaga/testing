import requests

BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_check_red_vs_green():
    response = requests.post(
        f"{BASE_URL}/check",
        headers={"Content-Type": "application/json"},
        json={"color1": "#FF0000", "color2": "#00FF00"}
    )
    assert response.status_code == 200
    assert response.json() == {"distinguishable": False}

def test_check_red_vs_blue():
    response = requests.post(
        f"{BASE_URL}/check",
        headers={"Content-Type": "application/json"},
        json={"color1": "#FF0000", "color2": "#0000FF"}
    )
    assert response.status_code == 200
    assert response.json() == {"distinguishable": True}

