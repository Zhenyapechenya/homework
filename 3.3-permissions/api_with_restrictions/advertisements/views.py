from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadonly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadonly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(creator=self.request.user)
        else:
            raise PermissionDenied(detail="Authentication required for this action.")

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsOwnerOrReadonly()]
        return []
