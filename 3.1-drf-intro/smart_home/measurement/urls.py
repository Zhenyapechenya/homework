from django.urls import path

from measurement.views import SensorsView, SensorChange

urlpatterns = [
    path('sensors/', SensorsView.as_view()),
    path('/sensors/<pk>/', SensorChange.as_view()),
    # TODO: зарегистрируйте необходимые маршруты
]
