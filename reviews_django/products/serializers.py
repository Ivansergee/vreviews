from rest_framework import serializers

from .models import Product, Brand, Producer, Flavor, Review, Comment


class FlavorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flavor
        fields = ['id', 'name']


class ProductProducerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Producer
        fields = ['name', 'country']


class BrandProductSerializer(serializers.ModelSerializer):
    flavors = FlavorSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'get_absolute_url', 'get_image', 'flavors']


class BrandSerializer(serializers.ModelSerializer):
    producer = ProductProducerSerializer()
    products = BrandProductSerializer(many=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'description', 'slug', 'get_image', 'producer', 'products']


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
        fields = ['id', 'name', 'description', 'slug', 'get_image', 'brand', 'flavors']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'review', 'text', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'product', 'score', 'text']


class ProductReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True)

    class Meta:
        model = Review
        fields = ['id', 'author', 'score', 'text', 'created_at', 'comments']
