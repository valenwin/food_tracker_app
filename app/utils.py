def total_by_food_element(food):
    total = {
        'protein': 0,
        'carbohydrates': 0,
        'fat': 0,
        'calories': 0
    }
    for item in food:
        total['protein'] += item.protein
        total['carbohydrates'] += item.carbohydrates
        total['fat'] += item.fat
        total['calories'] += item.calories
    return total
