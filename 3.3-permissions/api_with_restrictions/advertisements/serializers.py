from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement, FavoriteAdvertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', 'is_favorite')

    def create(self, validated_data):
        """Метод для создания"""
        
        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        user = self.context['request'].user
        if Advertisement.objects.filter(creator=user, status='OPEN').count() >= 10 and data.get('status') not in ['CLOSED', 'DRAFT']:
            raise serializers.ValidationError("У вас уже есть 10 открытых объявлений.")
        return data

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return FavoriteAdvertisement.objects.filter(user=user, advertisement=obj).exists()
        return False
    

class FavoriteAdvertisementSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='advertisement.title')
    description = serializers.CharField(source='advertisement.description')
    creator = serializers.PrimaryKeyRelatedField(source='advertisement.creator', read_only=True)
    status = serializers.CharField(source='advertisement.status')
    created_at = serializers.DateTimeField(source='advertisement.created_at')

    # Добавляем поле is_favorite, которое уже есть в модели FavoriteAdvertisement
    is_favorite = serializers.BooleanField(default=True)

    class Meta:
        model = FavoriteAdvertisement
        fields = ['advertisement', 'created_at', 'title', 'description', 'creator', 'status', 'created_at', 'is_favorite']