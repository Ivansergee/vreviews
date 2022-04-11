from rest_framework import serializers

from .models import Product, Brand, Producer, Flavor


class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = ['id', 'name']

class ProductProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['name', 'country']

class BrandSerializer(serializers.ModelSerializer):
    producer = ProductProducerSerializer()

    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'get_image', 'producer']

class ProductBrandSerializer(serializers.ModelSerializer):
    producer = ProductProducerSerializer()

    class Meta:
        model = Brand
        fields = ['name', 'producer']

class ProductSerializer(serializers.ModelSerializer):
    brand = ProductBrandSerializer()
    flavors = FlavorSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'get_absolute_url', 'get_image', 'brand', 'flavors']