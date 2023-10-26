from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorSerializer

# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView


# @api_view(['GET', 'POST'])
# def demo(request):
#     if request.method == 'GET':
#         weapons = Weapon.objects.all()
#         ser = WeaponSerializer(weapons, many=True)
#         return Response(ser.data)
    
#     if request.method == 'POST':
#         return Response({'status': 'ok'})
    



# class DemoView(APIView):
#     def get(self, request):
#         weapons = Weapon.objects.all()
#         ser = WeaponSerializer(weapons, many=True)
#         return Response(ser.data)
    
#     def post(self, request):
#         return Response({'status': 'ok'})

###########################################################
# class DemoView(generics.ListAPIView):
#     queryset = Weapon.objects.all()
#     serializer_class = WeaponSerializer

#     def post(self, request):
#         return Response({'status': 'ok'})
    

# class WeaponView(generics.RetrieveAPIView):
#     queryset = Weapon.objects.all()
#     serializer_class = WeaponSerializer

############################################################



class SensorsView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def post(self, request):
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SensorChange(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer  #надо будет изменить сериалайзер для подробной информации об объекте
