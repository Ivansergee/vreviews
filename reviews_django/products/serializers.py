from rest_framework import serializers

from .models import Product, Brand, Producer, Flavor, Review, Comment, Reaction


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
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'review', 'text', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'product', 'score', 'text']


class ReactionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reaction
        fields = ['id', 'author', 'review', 'like']


class ProductReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True)
    likes_count = serializers.IntegerField()
    dislikes_count = serializers.IntegerField()
    user_reaction = serializers.BooleanField()

    class Meta:
        model = Review
        fields = ['id', 'author', 'score', 'text', 'created_at', 'likes_count', 'dislikes_count', 'user_reaction', 'comments']
