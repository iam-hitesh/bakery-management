from django.contrib.auth import get_user_model

from rest_framework import serializers

import bakery.models as models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']


class BakeryIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BakeryIngredient
        fields = '__all__'


class BakeryItemIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BakeryItemIngredient
        fields = '__all__'


class BakeryItemSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.BakeryItem
        fields = '__all__'

    def get_ingredients(self, object):
        data = models.BakeryItemIngredient.objects.filter(bakery_item=object)
        serializer = BakeryItemIngredientSerializer(data, many=True)

        return serializer.data


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = '__all__'
