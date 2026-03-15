from rest_framework import serializers

from .models import Category, CategoryImage


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ["id", "image", "product"]


class CategorySerializer(serializers.ModelSerializer):
    images = CategoryImageSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "products", "images"]
