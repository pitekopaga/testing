import requests

BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_login_page_loads():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "Color Vision Diagnostic Test" in response.text
    assert "username" in response.text

def test_form_submission_redirects():
    # Start a session to maintain cookies
    session = requests.Session()
    response = session.get(f"{BASE_URL}/")
    assert response.status_code == 200
    
    # Submit a login
    response = session.post(f"{BASE_URL}/", data={"username": "testuser"})
    assert response.status_code == 302  # Redirect to test page
    
    # Follow redirect
    response = session.get(response.headers['Location'])
    assert response.status_code == 200
    assert "Plate 1 of" in response.text

def test_debug_stats_endpoint():
    response = requests.get(f"{BASE_URL}/debug/stats")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "cpu_percent" in data
    assert "memory_percent" in data
