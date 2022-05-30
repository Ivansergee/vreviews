from rest_framework import serializers

from .models import Product, Brand, Producer, Review, Comment, Reaction, Flavor, Nicotine


class FlavorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flavor
        fields = ['id', 'name']


class BrandNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'name']


class NicotineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nicotine
        fields = ['id', 'amount']


class ProducerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Producer
        fields = ['name', 'country', 'slug']


class BrandProductSerializer(serializers.ModelSerializer):
    flavors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'slug',
            'get_absolute_url',
            'get_image',
            'flavors',
            'get_reviews_amount',
            'get_avg_score',
            'get_score_amount'
        ]


class BrandDetailSerializer(serializers.ModelSerializer):
    producer = ProducerSerializer()
    products = BrandProductSerializer(many=True)

    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'get_image',
            'get_reviews_amount',
            'get_avg_score',
            'get_score_amount',
            'producer',
            'products'
        ]


class ProductBrandSerializer(serializers.ModelSerializer):
    producer = ProducerSerializer()

    class Meta:
        model = Brand
        fields = ['name', 'producer']


class ProductSerializer(serializers.ModelSerializer):
    brand = ProductBrandSerializer()
    flavors = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'brand',
            'flavors',
            'nic_content',
            'is_salt',

            'get_image',
            'get_absolute_url',
            'get_reviews_amount',
            'get_avg_score',
            'get_score_amount'
        ]

class CreateProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'slug',
            'image',
            'brand',
            'is_salt',
            'nic_content',
            'flavors',
        ]


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
    user_reaction = serializers.NullBooleanField()

    class Meta:
        model = Review
        fields = ['id', 'author', 'score', 'text', 'created_at', 'likes_count', 'dislikes_count', 'user_reaction', 'comments']
