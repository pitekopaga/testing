import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            pass
        yield client

def test_result_page_returns_200(client):
    """Test that the result page loads without crashing."""
    # The result page redirects to index if no session, but should not crash
    response = client.get('/result')
    assert response.status_code in [200, 302]

def test_health_endpoint_returns_ok(client):
    """Test that the health endpoint works."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {'status': 'ok'}

def test_debug_stats_endpoint_returns_stats(client):
    """Test that the debug stats endpoint returns expected fields."""
    response = client.get('/debug/stats')
    assert response.status_code == 200
    data = response.json
    assert 'status' in data
    assert 'cpu_percent' in data
    assert 'memory_percent' in data
    assert 'active_sessions' in data
