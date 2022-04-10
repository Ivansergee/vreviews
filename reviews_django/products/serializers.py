from rest_framework import serializers

from .models import Product, Brand, Producer, Flavor


class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = ['id', 'name']

class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ['id', 'name', 'country', 'description']

class BrandSerializer(serializers.ModelSerializer):
    producer = ProducerSerializer()

    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'get_absolute_url', 'get_image', 'producer']

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    flavors = FlavorSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'get_absolute_url', 'get_image', 'brand', 'flavors']