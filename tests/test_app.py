import json
import pytest
from app import app, validate_input, compute_scores, identify_primary_leak, get_persona, generate_mission_payload
from werkzeug.exceptions import BadRequest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ==============================================================================
# Helper Function Tests
# ==============================================================================

def test_validate_input_success():
    payload = {
        'transport': 'car',
        'food': 'food_delivery',
        'energy': 'ac_above_8',
        'shopping': 'frequent'
    }
    t, f, e, s = validate_input(payload)
    assert (t, f, e, s) == ('car', 'food_delivery', 'ac_above_8', 'frequent')

def test_validate_input_missing_keys():
    # Should use defaults
    t, f, e, s = validate_input({})
    assert (t, f, e, s) == ('walking', 'vegetarian', 'ac_under_2', 'rarely')

def test_validate_input_invalid_category():
    payload = {'transport': 'spaceship'}
    with pytest.raises(BadRequest) as excinfo:
        validate_input(payload)
    assert 'Invalid transport category' in str(excinfo.value)

def test_compute_scores():
    keys = ('walking', 'vegetarian', 'ac_under_2', 'rarely')
    scores = compute_scores(keys)
    assert scores['transport']['score'] == 0
    assert scores['food']['score'] == 10
    assert scores['energy']['score'] == 5
    assert scores['shopping']['score'] == 5

def test_identify_primary_leak():
    scores = {
        'transport': {'score': 10},
        'food': {'score': 30},
        'energy': {'score': 50},
        'shopping': {'score': 20}
    }
    category, score, label = identify_primary_leak(scores)
    assert category == 'energy'
    assert score == 50

def test_get_persona():
    persona = get_persona(20, 'transport', 'vegetarian')
    assert persona['name'] == 'Conscious Consumer'
    
    persona = get_persona(80, 'food', 'food_delivery')
    assert persona['name'] == 'Delivery Devotee'

# ==============================================================================
# Endpoint Tests
# ==============================================================================

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
    
    # Energy 'ac_above_8' (score 50) is higher than Food 'food_delivery' (score 30)
    assert data['leak_category'] == 'Energy'
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
    assert response.status_code in [400, 415]
    if response.status_code == 400:
        data = json.loads(response.data)
        assert 'error' in data

def test_analyze_invalid_category_endpoint(client):
    """Test validation blocks invalid category keys."""
    payload = {'transport': 'spaceship'}
    response = client.post('/api/analyze', json=payload)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Invalid transport category' in data['message']

def test_fallback_behavior_endpoint(client):
    """Test behavior when user submits minimal viable data (defaults)."""
    response = client.post('/api/analyze', json={})
    assert response.status_code == 200
    data = json.loads(response.data)
    
    # Using defaults (walking, veg, ac<2, rarely) -> overall score = 0+10+5+5 = 20
    assert data['leak_name'] == 'Eco Champion Status'
    assert data['simulation']['total_current'] == 20
