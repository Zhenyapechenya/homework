from rest_framework import serializers

from measurement.models import Weapon



# TODO: опишите необходимые сериализаторы


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = ['id', 'power', 'rarity']