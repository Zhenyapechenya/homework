from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from measurement.models import Weapon
from measurement.serializers import WeaponSerializer

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


class DemoView(generics.ListAPIView):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer

    def post(self, request):
        return Response({'status': 'ok'})
    

class WeaponView(generics.RetrieveAPIView):
    queryset = Weapon.objects.all()
    serializer_class = WeaponSerializer