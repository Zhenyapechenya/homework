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
    # можете добавить свои рецепты ;)
}


def get_recipe(request, dish):
    servings = int(request.GET.get('servings', 1))
    ingredients = DATA.get(dish)
    for value in ingredients.values():
        value = value * servings

    ingredients['яйца, шт'] = ingredients['яйца, шт'] * servings
    print(ingredients)
    
    context = {
        'recipe': ingredients,
        'servings': servings
    }
    print(servings)
    return render(request, 'demo.html', context)
