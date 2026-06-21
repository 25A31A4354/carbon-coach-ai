import os
from typing import Tuple, Dict, Any, List
from flask import Flask, render_template, request, jsonify
from werkzeug.exceptions import BadRequest

from constants import (
    TRANSPORT_SCORES, FOOD_SCORES, ENERGY_SCORES, SHOPPING_SCORES,
    MISSIONS, DEFAULT_MISSION,
    PERSONA_CONSCIOUS, PERSONAS_BY_CATEGORY, PERSONAS_BY_FOOD
)

app = Flask(__name__)

# ==============================================================================
# Error Handlers
# ==============================================================================

@app.errorhandler(400)
def bad_request(error: Exception) -> Tuple[Any, int]:
    """Handle 400 Bad Request errors gracefully."""
    return jsonify({
        'error': 'Bad Request', 
        'message': str(error.description if hasattr(error, 'description') else error)
    }), 400

@app.errorhandler(500)
def internal_error(error: Exception) -> Tuple[Any, int]:
    """Handle 500 Internal Server errors gracefully."""
    return jsonify({
        'error': 'Internal Server Error', 
        'message': 'An unexpected error occurred.'
    }), 500

# ==============================================================================
# Business Logic Helpers
# ==============================================================================

def validate_input(data: Dict[str, Any]) -> Tuple[str, str, str, str]:
    """
    Validate incoming payload keys and types.
    
    Args:
        data: The JSON payload dictionary.
        
    Returns:
        Tuple of sanitized keys: (transport_key, food_key, energy_key, shopping_key)
        
    Raises:
        BadRequest: If payload is missing or contains invalid keys.
    """
    if data is None or not isinstance(data, dict):
        raise BadRequest("Invalid or missing JSON payload.")
    
    transport_key = data.get('transport', 'walking')
    food_key = data.get('food', 'vegetarian')
    energy_key = data.get('energy', 'ac_under_2')
    shopping_key = data.get('shopping', 'rarely')
    
    if transport_key not in TRANSPORT_SCORES:
        raise BadRequest(f"Invalid transport category: {transport_key}")
    if food_key not in FOOD_SCORES:
        raise BadRequest(f"Invalid food category: {food_key}")
    if energy_key not in ENERGY_SCORES:
        raise BadRequest(f"Invalid energy category: {energy_key}")
    if shopping_key not in SHOPPING_SCORES:
        raise BadRequest(f"Invalid shopping category: {shopping_key}")
        
    return transport_key, food_key, energy_key, shopping_key


def compute_scores(keys: Tuple[str, str, str, str]) -> Dict[str, Dict[str, Any]]:
    """
    Look up the exact scores and metadata for the provided keys.
    
    Args:
        keys: Tuple of (transport_key, food_key, energy_key, shopping_key)
        
    Returns:
        Dictionary containing resolved data for each category.
    """
    t_key, f_key, e_key, s_key = keys
    return {
        'transport': TRANSPORT_SCORES[t_key],
        'food': FOOD_SCORES[f_key],
        'energy': ENERGY_SCORES[e_key],
        'shopping': SHOPPING_SCORES[s_key]
    }


def identify_primary_leak(scores_data: Dict[str, Dict[str, Any]]) -> Tuple[str, int, str]:
    """
    Identify the category contributing the highest carbon score.
    
    Args:
        scores_data: Resolved scores dictionary from compute_scores.
        
    Returns:
        Tuple containing (category_key, max_score, display_label).
    """
    categories = [
        ('transport', scores_data['transport']['score'], 'Transport'),
        ('food', scores_data['food']['score'], 'Food'),
        ('energy', scores_data['energy']['score'], 'Energy'),
        ('shopping', scores_data['shopping']['score'], 'Shopping')
    ]
    
    # Sort descending by score
    categories.sort(key=lambda x: x[1], reverse=True)
    return categories[0]


def get_persona(total_score: int, max_category: str, food_key: str) -> Dict[str, str]:
    """
    Determine a personalized carbon persona based on user habits.
    
    Args:
        total_score: The total sum of carbon scores.
        max_category: The category with the highest emission score.
        food_key: The specific choice made in the food category.
        
    Returns:
        Dictionary containing persona name, description, and opportunity.
    """
    if total_score <= 25:
        return PERSONA_CONSCIOUS
    
    if max_category in PERSONAS_BY_CATEGORY:
        return PERSONAS_BY_CATEGORY[max_category]
    
    if max_category == "food":
        if food_key == 'food_delivery':
            return PERSONAS_BY_FOOD['food_delivery']
        return PERSONAS_BY_FOOD['default']
        
    # Fallback
    return PERSONA_CONSCIOUS


def generate_mission_payload(max_category: str, max_score: int, keys: Tuple[str, str, str, str], scores_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate mission parameters using centralized dictionary mappings.
    
    Args:
        max_category: The primary leak category.
        max_score: The score of the primary leak.
        keys: Tuple of (transport_key, food_key, energy_key, shopping_key)
        scores_data: The resolved scoring data.
        
    Returns:
        Dictionary of formatted output variables (mission, savings, future scores, etc.)
    """
    t_key, f_key, e_key, s_key = keys
    
    # Initialize base variables with defaults
    mission_data = DEFAULT_MISSION.copy()
    
    future_scores = {
        'transport': scores_data['transport']['score'],
        'food': scores_data['food']['score'],
        'energy': scores_data['energy']['score'],
        'shopping': scores_data['shopping']['score']
    }
    
    if max_score > 20:
        # Determine specific trigger key for the max category
        specific_key = {
            'transport': t_key,
            'food': f_key,
            'energy': e_key,
            'shopping': s_key
        }.get(max_category)
        
        # Load category missions mapping
        cat_missions = MISSIONS.get(max_category, {})
        
        # Check if the specific key triggers the "high" impact mission
        selected_mission = cat_missions.get('default', {})
        if specific_key in cat_missions.get('high', {}).get('trigger_keys', []):
            selected_mission = cat_missions['high']
            
        if selected_mission:
            mission_data.update({
                'leak_name': selected_mission['leak_name'],
                'leak_category': max_category.capitalize(),
                'reason': selected_mission['reason'],
                'impact_pct': selected_mission['impact_pct'],
                'mission': selected_mission['mission'],
                'motivation': selected_mission['motivation'],
                'difficulty': selected_mission['difficulty'],
                'savings': selected_mission['savings']
            })
            
            # Apply future score override
            override = selected_mission['future_score_override']
            if override < 0:
                # Relative reduction
                future_scores[max_category] = max(0, future_scores[max_category] + override)
            else:
                # Absolute replacement
                future_scores[max_category] = override

    return mission_data, future_scores

# ==============================================================================
# Routes
# ==============================================================================

@app.route('/')
def index() -> str:
    """Serve the main frontend application."""
    return render_template('index.html')


@app.route('/api/analyze', methods=['POST'])
def analyze() -> Any:
    """Analyze the user's footprint and return missions and insights."""
    data = request.get_json()
    
    # Phase 1 & 2: Modularized logic and safe validation
    keys = validate_input(data)
    scores_data = compute_scores(keys)
    
    max_category, max_score, max_label = identify_primary_leak(scores_data)
    
    # Generate tailored mission
    mission_data, future_scores = generate_mission_payload(max_category, max_score, keys, scores_data)
    
    total_current = sum(s['score'] for s in scores_data.values())
    total_future = sum(future_scores.values())
    
    persona = get_persona(total_current, max_category, keys[1]) # keys[1] is food_key
    
    m_reasoning = f"Based on your habits, your biggest carbon leak is {mission_data['leak_category']}. This mission was chosen because it provides the highest reduction opportunity with minimal lifestyle disruption."
    impact_severity = "High" if max_score >= 40 else "Medium" if max_score >= 20 else "Low"
    
    # Assemble the final response
    result = {
        'leak_name': mission_data['leak_name'],
        'leak_category': mission_data['leak_category'],
        'reason': mission_data['reason'],
        'impact_pct': mission_data['impact_pct'],
        'impact_severity': impact_severity,
        'weekly_mission': mission_data['mission'],
        'future_insight': "You are making a significant choice to prioritize the planet. Keep going!",
        'motivation': mission_data['motivation'],
        'mission_reasoning': m_reasoning,
        'difficulty_level': mission_data['difficulty'],
        'estimated_savings': mission_data['savings'],
        'persona': persona,
        'simulation': {
            'categories': [
                {
                    'name': 'Transport',
                    'current': scores_data['transport']['score'],
                    'future': future_scores['transport'],
                    'label_current': scores_data['transport']['label'],
                    'icon': scores_data['transport']['icon']
                },
                {
                    'name': 'Food',
                    'current': scores_data['food']['score'],
                    'future': future_scores['food'],
                    'label_current': scores_data['food']['label'],
                    'icon': scores_data['food']['icon']
                },
                {
                    'name': 'Energy',
                    'current': scores_data['energy']['score'],
                    'future': future_scores['energy'],
                    'label_current': scores_data['energy']['label'],
                    'icon': scores_data['energy']['icon']
                },
                {
                    'name': 'Shopping',
                    'current': scores_data['shopping']['score'],
                    'future': future_scores['shopping'],
                    'label_current': scores_data['shopping']['label'],
                    'icon': scores_data['shopping']['icon']
                }
            ],
            'total_current': total_current,
            'total_future': total_future
        }
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
