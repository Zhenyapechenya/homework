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

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }


def get_recipe(request, dish):
    recipe = DATA.get(dish)
    return HttpResponse(f'Sum = {recipe}')

# def get_recipe(request):
#     name = request.GET.get('name')
#     age = int(request.GET.get('age', 20))
#     print(age)
#     return HttpResponse(f'hi, {name}')

# def sum(request, a, b):
#     result = a + b
#     return HttpResponse(f'Sum = {result}')


def hello(request):
    return render(request, 'demo.html')