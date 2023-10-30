from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer, ShowSensorSerializer, SensorDetailSerializer, MeasurementCreateSerializer



class SensorsView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = ShowSensorSerializer  # посмотреть список датчиков

    def post(self, request):  # создать датчик
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorChange(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer  # для подробной информации об объекте

    def patch(self, request, *args, **kwargs):  # изменить датчик
        partial_serializer = SensorSerializer(data=request.data, partial=True)
        if partial_serializer.is_valid():
            return super().patch(request, *args, **kwargs)
        else:
            return Response(partial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class MeasurementCreate(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementCreateSerializer  # создать измерение
    from rest_framework.parsers import MultiPartParser