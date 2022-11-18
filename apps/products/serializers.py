from rest_framework import serializers

from apps.products.models import Product


class ProductCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_title', 'product_description', 'price']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_title', 'price', 'seller']


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_title', 'product_description', 'price', 'date_listed']


class ProductUpdateSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(max_length=256)
    product_description = serializers.CharField(max_length=1024)

    class Meta:
        model = Product
        fields = ['product_title', 'product_description', 'price']
