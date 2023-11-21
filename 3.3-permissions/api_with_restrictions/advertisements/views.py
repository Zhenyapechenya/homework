from django_filters.rest_framework import DjangoFilterBackend, DateFromToRangeFilter, FilterSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement, AdvertisementStatusChoices, FavoriteAdvertisement
from advertisements.permissions import IsOwnerOrReadonly
from advertisements.serializers import AdvertisementSerializer, FavoriteAdvertisementSerializer



class AdvertisementFilter(FilterSet):
    created_at = DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['creator', 'created_at', 'status']



class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    permission_classes = [IsAuthenticated, IsOwnerOrReadonly]


    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied(detail="Authentication required for this action.")


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'retrieve', 'list']:
            return [IsOwnerOrReadonly()]
        return []


    @action(detail=True, methods=['post'])
    def add_to_favorites(self, request, pk=None):
        advertisement = self.get_object()

        if request.user.is_authenticated:
            # Проверяем, что объявление не принадлежит текущему пользователю
            if advertisement.creator == request.user:
                return Response({"detail": "Нельзя добавить своё объявление в избранное."}, status=status.HTTP_400_BAD_REQUEST)

            # Проверяем, что объявление уже добавлено в избранное пользователем
            try:
                favorite_advertisement = FavoriteAdvertisement.objects.get(user=request.user, advertisement=advertisement)
                # Если объявление уже в избранном, удаляем его из избранного
                favorite_advertisement.delete()
                return Response({"detail": "Объявление удалено из избранного."}, status=status.HTTP_200_OK)
            except FavoriteAdvertisement.DoesNotExist:
                # Если объявление не в избранном, добавляем его в избранное
                FavoriteAdvertisement.objects.create(user=request.user, advertisement=advertisement)
                return Response({"detail": "Объявление добавлено в избранное."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Необходима аутентификация для добавления в избранное."}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'])
    def favorite_advertisements(self, request):
        # Проверяем, аутентифицирован ли пользователь
        if request.user.is_authenticated:
            # Получаем избранные объявления для пользователя
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
        