# Core Carbon Score mappings

TRANSPORT_SCORES = {
    'walking': {'score': 0, 'label': 'Walking'},
    'bicycle': {'score': 0, 'label': 'Bicycle'},
    'public_transport': {'score': 15, 'label': 'Public Transport'},
    'bike_scooter': {'score': 35, 'label': 'Bike/Scooter'},
    'car': {'score': 90, 'label': 'Car Travel'}
}

FOOD_SCORES = {
    'vegetarian': {'score': 10, 'label': 'Vegetarian'},
    'mixed': {'score': 35, 'label': 'Mixed Diet'},
    'mostly_non_veg': {'score': 75, 'label': 'Mostly Non-Veg'},
    'food_delivery': {'score': 95, 'label': 'Food Delivery'}
}

ENERGY_SCORES = {
    'ac_under_2': {'score': 5, 'label': 'AC < 2 hrs'},
    'ac_2_5': {'score': 30, 'label': 'AC 2-5 hrs'},
    'ac_5_8': {'score': 65, 'label': 'AC 5-8 hrs'},
    'ac_above_8': {'score': 100, 'label': 'AC > 8 hrs'}
}

SHOPPING_SCORES = {
    'rarely': {'score': 5, 'label': 'Rarely'},
    'monthly': {'score': 20, 'label': 'Monthly'},
    'weekly': {'score': 55, 'label': 'Weekly'},
    'frequent': {'score': 90, 'label': 'Frequent'}
}
