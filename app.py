import os
import json
from typing import Tuple, Dict, Any
from flask import Flask, render_template, request, jsonify

from config import TRANSPORT_SCORES, FOOD_SCORES, ENERGY_SCORES, SHOPPING_SCORES

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(error: Exception) -> Tuple[Any, int]:
    """Handle 400 Bad Request errors gracefully."""
    return jsonify({'error': 'Bad Request', 'message': str(error.description if hasattr(error, 'description') else error)}), 400

@app.errorhandler(500)
def internal_error(error: Exception) -> Tuple[Any, int]:
    """Handle 500 Internal Server errors gracefully."""
    return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred.'}), 500

def get_persona(total_score: int, max_category: str, transport_key: str, food_key: str) -> Tuple[str, str, str]:
    """Determine a persona based on user scores."""
    if total_score <= 25:
        return "Conscious Consumer", "You are highly mindful of your environmental impact, consistently making sustainable choices.", "Advocate for sustainability and share your habits with your community."
    
    if max_category == "transport":
        return "Urban Commuter", "You rely significantly on motorized transit for daily movement, which forms the bulk of your footprint.", "Shift towards active mobility (walking/cycling) or public transit for short trips."
    elif max_category == "energy":
        return "Energy Heavy User", "Your reliance on climate control and home power forms the largest part of your environmental impact.", "Optimize thermostat settings and leverage natural ventilation."
    elif max_category == "shopping":
        return "Convenience Seeker", "You frequently make purchases, contributing to global supply chain and manufacturing emissions.", "Adopt a mindful 48-hour cooling-off period before non-essential purchases."
    else:
        if food_key == 'food_delivery':
            return "Delivery Devotee", "Your frequent reliance on food delivery adds significant emissions from packaging and transport.", "Incorporate more simple, home-cooked meals into your weekly routine."
        else:
            return "Dietary Impact User", "Your diet, particularly meat consumption, is the primary driver of your carbon footprint.", "Incorporate more plant-based meals into your weekly diet."



@app.route('/')
def index() -> str:
    """Serve the main frontend application."""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze() -> Any:
    """Analyze the user's footprint and return missions and insights."""
    from werkzeug.exceptions import BadRequest
    
    data = request.get_json()
    if data is None:
        raise BadRequest("Invalid or missing JSON payload.")
    
    transport_key = data.get('transport', 'walking')
    food_key = data.get('food', 'vegetarian')
    energy_key = data.get('energy', 'ac_under_2')
    shopping_key = data.get('shopping', 'rarely')
    
    # Input validation
    if transport_key not in TRANSPORT_SCORES:
        raise BadRequest(f"Invalid transport category: {transport_key}")
    if food_key not in FOOD_SCORES:
        raise BadRequest(f"Invalid food category: {food_key}")
    if energy_key not in ENERGY_SCORES:
        raise BadRequest(f"Invalid energy category: {energy_key}")
    if shopping_key not in SHOPPING_SCORES:
        raise BadRequest(f"Invalid shopping category: {shopping_key}")
    
    # Resolve scores
    t_data = TRANSPORT_SCORES.get(transport_key, TRANSPORT_SCORES['walking'])
    f_data = FOOD_SCORES.get(food_key, FOOD_SCORES['vegetarian'])
    e_data = ENERGY_SCORES.get(energy_key, ENERGY_SCORES['ac_under_2'])
    s_data = SHOPPING_SCORES.get(shopping_key, SHOPPING_SCORES['rarely'])
    
    scores = {
        'transport': t_data['score'],
        'food': f_data['score'],
        'energy': e_data['score'],
        'shopping': s_data['score']
    }
    
    # Find the category with the highest carbon footprint score (the leak)
    categories = [
        ('transport', scores['transport'], 'Transport'),
        ('food', scores['food'], 'Food'),
        ('energy', scores['energy'], 'Energy'),
        ('shopping', scores['shopping'], 'Shopping')
    ]
    
    categories.sort(key=lambda x: x[1], reverse=True)
    max_category, max_score, max_label = categories[0]
    
    # Default outputs
    leak_name = "Eco Champion Status"
    leak_category = "General"
    fallback_reason = "Your carbon footprint is already exceptionally low. You walk or cycle, eat a plant-based diet, conserve air conditioning, and shop mindfully."
    impact_pct = 5
    fallback_mission = "Incite eco-action: Share a vegetarian home-cooked recipe with a friend or neighbor."
    fallback_motivation = "Maintaining a low carbon lifestyle sets a positive example for global sustainability."
    fallback_difficulty = "Low"
    fallback_savings = "₹0/week"
    future_scores = scores.copy()
    
    if max_score > 20:
        if max_category == 'food' and food_key == 'food_delivery':
            leak_name = "Frequent Food Delivery"
            leak_category = "Food"
            fallback_reason = "Ordering delivery results in excessive emissions from single-portion motorcycle transit, redundant plastic packaging, and restaurant energy intensity. Swapping these for simple home-cooked meals yields immediate impact."
            impact_pct = 28
            fallback_mission = "Replace 2 restaurant food deliveries with quick home-cooked meals."
            fallback_motivation = "Reducing delivery cuts packaging waste and delivery vehicle emissions."
            fallback_difficulty = "Medium"
            fallback_savings = "₹300–₹500/week"
            future_scores['food'] = 35
            
        elif max_category == 'transport' and transport_key == 'car':
            leak_name = "Daily Car Usage"
            leak_category = "Transport"
            fallback_reason = "Driving a single-occupant fossil-fuel car remains the largest driver of individual emissions. Short local trips are particularly carbon-intensive due to engine warm-up phases."
            impact_pct = 35
            fallback_mission = "Walk, cycle, or use transit for trips under 2 miles twice this week."
            fallback_motivation = "Walking short distances eliminates cold-engine emissions, which are highly polluting."
            fallback_difficulty = "High"
            fallback_savings = "₹100–₹300/week"
            future_scores['transport'] = 30
            
        elif max_category == 'energy' and energy_key in ['ac_above_8', 'ac_5_8']:
            leak_name = "Excessive AC Usage"
            leak_category = "Energy"
            fallback_reason = "Running high-wattage air conditioning for long hours creates a massive electrical demand, typically powered by fossil fuels, and accelerates the release of high-warming chemical refrigerants."
            impact_pct = 22
            fallback_mission = "Reduce AC runtime by 1.5 hours daily or raise the thermostat by 2°C (3.6°F)."
            fallback_motivation = "Lowering AC usage reduces fossil-fuel electrical demand and grid strain."
            fallback_difficulty = "Low"
            fallback_savings = "₹150–₹400/month"
            future_scores['energy'] = scores['energy'] - 30
            
        elif max_category == 'shopping' and shopping_key in ['frequent', 'weekly']:
            leak_name = "Frequent Shopping"
            leak_category = "Shopping"
            fallback_reason = "Frequent purchasing triggers downstream supply chain carbon: raw material extraction, global manufacturing, shipping freight, and return logistics. Purchasing only what you need halts this cycle."
            impact_pct = 18
            fallback_mission = "Adopt a 48-hour cooling-off period before buying any non-essential item."
            fallback_motivation = "Buying less directly stops the carbon-intensive manufacturing and shipping cycle."
            fallback_difficulty = "Medium"
            fallback_savings = "₹500–₹1000/month"
            future_scores['shopping'] = 20
            
        else:
            if max_category == 'food':
                leak_name = "High-Meat Diet"
                leak_category = "Food"
                fallback_reason = "Livestock farming (especially beef and dairy) is highly resource-intensive, producing methane and requiring massive land clearing. Shifting to plant-based meals directly reduces agricultural pressure."
                impact_pct = 24
                fallback_mission = "Go completely plant-based (Vegetarian/Vegan) for 3 full days this week."
                fallback_motivation = "Plant-based meals drastically reduce agricultural methane and land use."
                fallback_difficulty = "High"
                fallback_savings = "₹200–₹400/week"
                future_scores['food'] = 15
            elif max_category == 'transport':
                leak_name = "Motorized Local Transit"
                leak_category = "Transport"
                fallback_reason = "Using a bike/scooter or public transport is better than a car, but there is still room to optimize using active mobility (walking/cycling) for short neighborhood routes."
                impact_pct = 12
                fallback_mission = "Walk or ride a manual bicycle instead of taking a scooter for short tasks."
                fallback_motivation = "Active mobility produces zero emissions and reduces urban congestion."
                fallback_difficulty = "Low"
                fallback_savings = "₹50–₹150/week"
                future_scores['transport'] = 10
            elif max_category == 'energy':
                leak_name = "Moderate AC Usage"
                leak_category = "Energy"
                fallback_reason = "Air conditioning even for 2-5 hours represents a significant portion of home power bills and grid emissions. Natural ventilation or fans can easily offset this during cooler hours."
                impact_pct = 10
                fallback_mission = "Use a natural cross-breeze or ceiling fan instead of turning on the AC today."
                fallback_motivation = "Using fans uses a fraction of the electricity of air conditioning."
                fallback_difficulty = "Low"
                fallback_savings = "₹100–₹250/month"
                future_scores['energy'] = 10
            elif max_category == 'shopping':
                leak_name = "Regular Shopping Purchases"
                leak_category = "Shopping"
                fallback_reason = "Shopping monthly or semi-regularly still introduces new product manufacturing footprints. Extending the life of what you own is a powerful tool."
                impact_pct = 8
                fallback_mission = "Repair, mend, or repurpose an item you already own instead of buying new."
                fallback_motivation = "Extending item life prevents the emissions from producing new replacements."
                fallback_difficulty = "Medium"
                fallback_savings = "₹200–₹500/month"
                future_scores['shopping'] = 5

    total_current = sum(scores.values())
    total_future = sum(future_scores.values())

    p_name, p_desc, p_opp = get_persona(total_current, max_category, transport_key, food_key)
    
    # Generate deterministic outputs
    reason = fallback_reason
    weekly_mission = fallback_mission
    motivation = fallback_motivation
    difficulty = fallback_difficulty
    savings = fallback_savings
    
    m_reasoning = f"Based on your habits, your biggest carbon leak is {leak_category}. This mission was chosen because it provides the highest reduction opportunity with minimal lifestyle disruption."
    
    future_insight = "You are making a significant choice to prioritize the planet. Keep going!"
    
    impact_severity = "High" if max_score >= 40 else "Medium" if max_score >= 20 else "Low"
    
    result = {
        'leak_name': leak_name,
        'leak_category': leak_category,
        'reason': reason,
        'impact_pct': impact_pct,
        'impact_severity': impact_severity,
        'weekly_mission': weekly_mission,
        'future_insight': future_insight,
        'motivation': motivation,
        'mission_reasoning': m_reasoning,
        'difficulty_level': difficulty,
        'estimated_savings': savings,
        'persona': {
            'name': p_name,
            'description': p_desc,
            'opportunity': p_opp
        },
        'simulation': {
            'categories': [
                {
                    'name': 'Transport',
                    'current': scores['transport'],
                    'future': future_scores['transport'],
                    'label_current': t_data['label'],
                    'icon': 'car-outline' if transport_key == 'car' else 'walk-outline'
                },
                {
                    'name': 'Food',
                    'current': scores['food'],
                    'future': future_scores['food'],
                    'label_current': f_data['label'],
                    'icon': 'fast-food-outline' if food_key == 'food_delivery' else 'restaurant-outline'
                },
                {
                    'name': 'Energy',
                    'current': scores['energy'],
                    'future': future_scores['energy'],
                    'label_current': e_data['label'],
                    'icon': 'thermometer-outline'
                },
                {
                    'name': 'Shopping',
                    'current': scores['shopping'],
                    'future': future_scores['shopping'],
                    'label_current': s_data['label'],
                    'icon': 'bag-handle-outline'
                }
            ],
            'total_current': total_current,
            'total_future': total_future
        }
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
