from django.forms import ValidationError
from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

    def validate_description(self, value):
        if 'satan' in value:
            raise ValidationError('Покайтесь!')
        return value


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id','address', 'positions']    


    def create(self, validated_data):
        positions = validated_data.pop('positions')

        stock = super().create(validated_data)
        for position_data in positions:
            StockProduct.objects.create(stock=stock, **position_data)

        return stock


    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for position_data in positions:
            StockProduct.objects.update_or_create(defaults={'quantity': position_data['quantity'], 
                                                            'price': position_data['price']}, 
                                                            product=position_data['product'], 
                                                            stock=stock)
        return stock
