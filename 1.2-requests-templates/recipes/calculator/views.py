from django.http import HttpResponse
from django.shortcuts import render


DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def get_recipe(request, dish):
    servings = int(request.GET.get('servings', 1))
    ingredients = DATA.get(dish).copy()

    for key in ingredients:
        ingredients[key] = DATA.get(dish)[key] * servings
    
    context = {
        'recipe': ingredients,
        'servings': servings
    }
 
    return render(request, 'demo.html', context)

