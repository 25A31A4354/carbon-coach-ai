"""
CarbonCoach AI Constants & Mapping Configurations
Centralized dictionary lookups for O(1) efficiency and clean separation of concerns.
"""

# ---------------------------------------------------------
# SCORES CONFIGURATION
# ---------------------------------------------------------

TRANSPORT_SCORES = {
    'walking': {'score': 0, 'label': 'Walking', 'icon': 'walk-outline'},
    'bicycle': {'score': 0, 'label': 'Bicycle', 'icon': 'walk-outline'},
    'public_transport': {'score': 15, 'label': 'Public Transport', 'icon': 'bus-outline'},
    'bike_scooter': {'score': 35, 'label': 'Bike/Scooter', 'icon': 'bicycle-outline'},
    'car': {'score': 90, 'label': 'Car Travel', 'icon': 'car-outline'}
}

FOOD_SCORES = {
    'vegetarian': {'score': 10, 'label': 'Vegetarian', 'icon': 'restaurant-outline'},
    'mixed': {'score': 35, 'label': 'Mixed Diet', 'icon': 'restaurant-outline'},
    'mostly_non_veg': {'score': 75, 'label': 'Mostly Non-Veg', 'icon': 'restaurant-outline'},
    'food_delivery': {'score': 95, 'label': 'Food Delivery', 'icon': 'fast-food-outline'}
}

ENERGY_SCORES = {
    'ac_under_2': {'score': 5, 'label': 'AC < 2 hrs', 'icon': 'thermometer-outline'},
    'ac_2_5': {'score': 30, 'label': 'AC 2-5 hrs', 'icon': 'thermometer-outline'},
    'ac_5_8': {'score': 65, 'label': 'AC 5-8 hrs', 'icon': 'thermometer-outline'},
    'ac_above_8': {'score': 100, 'label': 'AC > 8 hrs', 'icon': 'thermometer-outline'}
}

SHOPPING_SCORES = {
    'rarely': {'score': 5, 'label': 'Rarely', 'icon': 'bag-handle-outline'},
    'monthly': {'score': 20, 'label': 'Monthly', 'icon': 'bag-handle-outline'},
    'weekly': {'score': 55, 'label': 'Weekly', 'icon': 'bag-handle-outline'},
    'frequent': {'score': 90, 'label': 'Frequent', 'icon': 'bag-handle-outline'}
}

# ---------------------------------------------------------
# MISSION GENERATION MATRIX (Problem Alignment)
# ---------------------------------------------------------
# Structure: { 'category': { 'high_impact': {...}, 'low_impact': {...} } }

MISSIONS = {
    'food': {
        'high': {
            'trigger_keys': ['food_delivery'],
            'leak_name': "Frequent Food Delivery",
            'reason': "Ordering delivery results in excessive emissions from single-portion motorcycle transit, redundant plastic packaging, and restaurant energy intensity. As your coach, I recommend swapping these for simple home-cooked meals to yield an immediate and massive impact.",
            'impact_pct': 28,
            'mission': "Replace 2 restaurant food deliveries with quick home-cooked meals.",
            'motivation': "Reducing delivery cuts packaging waste and delivery vehicle emissions right at the source.",
            'difficulty': "Medium",
            'savings': "₹300–₹500/week",
            'future_score_override': 35
        },
        'default': {
            'leak_name': "High-Meat Diet",
            'reason': "Livestock farming is highly resource-intensive, producing methane and requiring massive land clearing. Shifting to plant-based meals directly reduces agricultural pressure—this is one of the easiest ways to scale down your footprint.",
            'impact_pct': 24,
            'mission': "Go completely plant-based (Vegetarian/Vegan) for 3 full days this week.",
            'motivation': "Plant-based meals drastically reduce agricultural methane and land use.",
            'difficulty': "High",
            'savings': "₹200–₹400/week",
            'future_score_override': 15
        }
    },
    'transport': {
        'high': {
            'trigger_keys': ['car'],
            'leak_name': "Daily Car Usage",
            'reason': "Driving a single-occupant fossil-fuel car remains the largest driver of individual emissions. Short local trips are particularly carbon-intensive due to engine warm-up phases. Let's tackle these short trips first.",
            'impact_pct': 35,
            'mission': "Walk, cycle, or use transit for trips under 2 miles twice this week.",
            'motivation': "Walking short distances eliminates cold-engine emissions, which are highly polluting.",
            'difficulty': "High",
            'savings': "₹100–₹300/week",
            'future_score_override': 30
        },
        'default': {
            'leak_name': "Motorized Local Transit",
            'reason': "Using a scooter or public transport is better than a car, but there is still room to optimize by relying on your own active mobility for short neighborhood routes.",
            'impact_pct': 12,
            'mission': "Walk or ride a manual bicycle instead of taking a scooter for short tasks.",
            'motivation': "Active mobility produces zero emissions and reduces urban congestion.",
            'difficulty': "Low",
            'savings': "₹50–₹150/week",
            'future_score_override': 10
        }
    },
    'energy': {
        'high': {
            'trigger_keys': ['ac_above_8', 'ac_5_8'],
            'leak_name': "Excessive AC Usage",
            'reason': "Running high-wattage air conditioning for long hours creates a massive electrical demand and accelerates the release of high-warming chemical refrigerants. Trimming this usage is the most effective adjustment you can make at home.",
            'impact_pct': 22,
            'mission': "Reduce AC runtime by 1.5 hours daily or raise the thermostat by 2°C (3.6°F).",
            'motivation': "Lowering AC usage reduces fossil-fuel electrical demand and grid strain.",
            'difficulty': "Low",
            'savings': "₹150–₹400/month",
            'future_score_override': -30  # Relative reduction
        },
        'default': {
            'leak_name': "Moderate AC Usage",
            'reason': "Air conditioning even for 2-5 hours represents a significant portion of home power bills and grid emissions. Utilizing natural ventilation can easily offset this during cooler hours.",
            'impact_pct': 10,
            'mission': "Use a natural cross-breeze or ceiling fan instead of turning on the AC today.",
            'motivation': "Using fans uses a fraction of the electricity of air conditioning.",
            'difficulty': "Low",
            'savings': "₹100–₹250/month",
            'future_score_override': 10
        }
    },
    'shopping': {
        'high': {
            'trigger_keys': ['frequent', 'weekly'],
            'leak_name': "Frequent Shopping",
            'reason': "Frequent purchasing triggers downstream supply chain carbon: raw material extraction, global manufacturing, shipping freight, and return logistics. As your coach, I challenge you to halt this cycle temporarily.",
            'impact_pct': 18,
            'mission': "Adopt a 48-hour cooling-off period before buying any non-essential item.",
            'motivation': "Buying less directly stops the carbon-intensive manufacturing and shipping cycle.",
            'difficulty': "Medium",
            'savings': "₹500–₹1000/month",
            'future_score_override': 20
        },
        'default': {
            'leak_name': "Regular Shopping Purchases",
            'reason': "Shopping monthly or semi-regularly still introduces new product manufacturing footprints. Extending the life of what you already own is a powerful tool.",
            'impact_pct': 8,
            'mission': "Repair, mend, or repurpose an item you already own instead of buying new.",
            'motivation': "Extending item life prevents the emissions from producing new replacements.",
            'difficulty': "Medium",
            'savings': "₹200–₹500/month",
            'future_score_override': 5
        }
    }
}

# ---------------------------------------------------------
# DEFAULTS
# ---------------------------------------------------------

DEFAULT_MISSION = {
    'leak_name': "Eco Champion Status",
    'leak_category': "General",
    'reason': "Your carbon footprint is already exceptionally low. You walk or cycle, eat a plant-based diet, conserve air conditioning, and shop mindfully. Great work!",
    'impact_pct': 5,
    'mission': "Incite eco-action: Share a vegetarian home-cooked recipe with a friend or neighbor.",
    'motivation': "Maintaining a low carbon lifestyle sets a positive example for global sustainability.",
    'difficulty': "Low",
    'savings': "₹0/week"
}

# ---------------------------------------------------------
# PERSONAS
# ---------------------------------------------------------

PERSONA_CONSCIOUS = {
    'name': "Conscious Consumer",
    'description': "You are highly mindful of your environmental impact, consistently making sustainable choices.",
    'opportunity': "Advocate for sustainability and share your habits with your community."
}

PERSONAS_BY_CATEGORY = {
    'transport': {
        'name': "Urban Commuter",
        'description': "You rely significantly on motorized transit for daily movement, which forms the bulk of your footprint.",
        'opportunity': "Shift towards active mobility (walking/cycling) or public transit for short trips."
    },
    'energy': {
        'name': "Energy Heavy User",
        'description': "Your reliance on climate control and home power forms the largest part of your environmental impact.",
        'opportunity': "Optimize thermostat settings and leverage natural ventilation."
    },
    'shopping': {
        'name': "Convenience Seeker",
        'description': "You frequently make purchases, contributing to global supply chain and manufacturing emissions.",
        'opportunity': "Adopt a mindful 48-hour cooling-off period before non-essential purchases."
    }
}

PERSONAS_BY_FOOD = {
    'food_delivery': {
        'name': "Delivery Devotee",
        'description': "Your frequent reliance on food delivery adds significant emissions from packaging and transport.",
        'opportunity': "Incorporate more simple, home-cooked meals into your weekly routine."
    },
    'default': {
        'name': "Dietary Impact User",
        'description': "Your diet, particularly meat consumption, is the primary driver of your carbon footprint.",
        'opportunity': "Incorporate more plant-based meals into your weekly diet."
    }
}
