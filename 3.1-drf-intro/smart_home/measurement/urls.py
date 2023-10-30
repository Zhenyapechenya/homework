from django.urls import path

from measurement.views import SensorsView, SensorChange, MeasurementCreate

urlpatterns = [
    path('sensors/', SensorsView.as_view()),
    path('sensors/<pk>/', SensorChange.as_view()),
    path('measurements/', MeasurementCreate.as_view())
]
