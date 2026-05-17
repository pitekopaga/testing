import requests

BASE_URL = "http://localhost:5000"

def test_health_endpoint():
    """Test that health endpoint returns ok status"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_homepage_loads():
    """Test that the main test page loads correctly"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "Color Vision Diagnostic Test" in response.text
    assert "Enter number" in response.text

def test_form_submission():
    """Test that submitting an answer redirects correctly"""
    session = requests.Session()
    session.get(f"{BASE_URL}/")
    response = session.post(f"{BASE_URL}/", data={"answer": "0"})
    assert response.status_code in [200, 302]

def test_results_page():
    """Test that results page loads and shows scores"""
    session = requests.Session()
    session.get(f"{BASE_URL}/")
    
    response = None
    for _ in range(25):
        response = session.post(f"{BASE_URL}/", data={"answer": "0"})
        if "Your Color Blind Test Result" in response.text:
            break
    
    assert response is not None
    assert "Your Color Blind Test Result" in response.text
    assert "score" in response.text.lower() or "cone" in response.text.lower()
