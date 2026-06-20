import json
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_analyze_success(client):
    """Test successful analysis with valid inputs."""
    payload = {
        'transport': 'car',
        'food': 'food_delivery',
        'energy': 'ac_above_8',
        'shopping': 'frequent'
    }
    response = client.post('/api/analyze', json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Food Delivery should be the highest leak
    # Energy 'ac_above_8' (score 50) is higher than Food 'food_delivery' (score 30)
    assert data['leak_category'] == 'Energy'
    assert 'air conditioning' in str(data['reason']).lower() or 'energy' in str(data['reason']).lower()
    assert 'simulation' in data
    assert 'weekly_mission' in data
    assert 'impact_severity' in data
    assert 'motivation' in data
    assert 'persona' in data
    assert 'name' in data['persona']
    assert 'difficulty_level' in data
    assert 'estimated_savings' in data
    assert 'mission_reasoning' in data
    
def test_analyze_invalid_payload(client):
    """Test missing or invalid JSON payload."""
    response = client.post('/api/analyze', data="not a json")
    # Flask returns 415 Unsupported Media Type when JSON is expected but not provided
    assert response.status_code in [400, 415]
    if response.status_code == 400:
        data = json.loads(response.data)
        assert 'error' in data

def test_analyze_invalid_category(client):
    """Test validation blocks invalid category keys."""
    payload = {
        'transport': 'spaceship',
        'food': 'vegetarian',
        'energy': 'ac_under_2',
        'shopping': 'rarely'
    }
    response = client.post('/api/analyze', json=payload)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Invalid transport category' in data['message']

def test_fallback_behavior(client):
    """Test behavior when user submits minimal viable data (defaults)."""
    response = client.post('/api/analyze', json={})
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Using defaults (walking, veg, ac<2, rarely) -> overall score = 0+10+5+5 = 20
    assert data['leak_name'] == 'Eco Champion Status'
    assert data['simulation']['total_current'] == 20
