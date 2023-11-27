from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement, AdvertisementStatusChoices, FavoriteAdvertisement
from advertisements.permissions import IsOwnerOrReadonly
from advertisements.serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer
from advertisements.filters import AdvertisementFilter



class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadonly]


    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            if user.is_staff:
                return Advertisement.objects.filter(status__in=['OPEN', 'CLOSED'])
            else:
                return Advertisement.objects.filter(creator=user)
        else:
            return Advertisement.objects.filter(status__in=['OPEN', 'CLOSED'])


    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied(detail="Authentication required for this action.")


    @action(detail=True, methods=['post'])
    def add_to_favorites(self, request, pk=None):
        advertisement = self.get_object()

        if request.user.is_authenticated:
            if advertisement.creator == request.user:
                return Response({"detail": "Нельзя добавить своё объявление в избранное."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                favorite_advertisement = FavoriteAdvertisement.objects.get(user=request.user, advertisement=advertisement)
                favorite_advertisement.delete()
                return Response({"detail": "Объявление удалено из избранного."}, status=status.HTTP_200_OK)
            except FavoriteAdvertisement.DoesNotExist:
                FavoriteAdvertisement.objects.create(user=request.user, advertisement=advertisement)
                return Response({"detail": "Объявление добавлено в избранное."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Необходима аутентификация для добавления в избранное."}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'])
    def favorite_advertisements(self, request):
        if request.user.is_authenticated:
            favorite_advertisements = request.user.favorite_advertisements.all()
            serializer = FavoriteAdvertisementSerializer(favorite_advertisements, many=True)
            return Response(serializer.data)
        else:
            return Response({"detail": "Вы не аутентифицированы"}, status=status.HTTP_401_UNAUTHORIZED)
        
    
    # метод для просмотра объявлений только автору в режиме черновика
    @action(detail=True, methods=['get'], permission_classes=[IsOwnerOrReadonly])
    def draft(self, request, pk=None):
        advertisement = self.get_object()
        if advertisement.status == AdvertisementStatusChoices.DRAFT:
            serializer = AdvertisementSerializer(advertisement, context={'request': request})
            return Response(serializer.data)
        