from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Product, Brand, Producer, Review, Comment, Reaction, Flavor, Nicotine


class ProducerShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = ['name', 'slug', 'country']


class BrandShortSerializer(serializers.ModelSerializer):
    producer = ProducerShortSerializer(read_only=True)

    class Meta:
        model = Brand
        fields = ['name', 'slug', 'producer']


class FlavorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flavor
        fields = ['id', 'name']
        read_only_fields = 'name'


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandShortSerializer(read_only=True)
    flavors = serializers.StringRelatedField(many=True)
    nic_content = serializers.StringRelatedField(many=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        source='brand',
        write_only=True
        )
    flavor_id = serializers.PrimaryKeyRelatedField(
        queryset=Flavor.objects.all(),
        source='flavors',
        many=True,
        write_only=True
        )
    nic_content_id = serializers.PrimaryKeyRelatedField(
        queryset=Nicotine.objects.all(),
        source='nic_content',
        many=True,
        write_only=True
        )

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'brand',
            'brand_id',
            'flavors',
            'flavor_id',
            'nic_content',
            'nic_content_id',
            'is_salt',
            'image',

            'get_reviews_amount',
            'get_avg_score',
            'get_score_amount'
        ]
        read_only_fields = ['slug']

    def to_representation(self, instance):
        response = super(ProductSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class BrandSerializer(serializers.ModelSerializer):
    producer = ProducerShortSerializer(read_only=True)

    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'producer',
            'image',

            'get_reviews_amount',
            'get_avg_score',
            'get_score_amount',
        ]

    def to_representation(self, instance):
        response = super(BrandSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class ProducerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'image',

            'get_reviews_amount',
            'get_avg_score',
            'get_score_amount',
        ]

    def to_representation(self, instance):
        response = super(ProducerSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'review', 'text', 'created_at']
        read_only_fields = ['review']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    product = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)
    user_reaction = serializers.NullBooleanField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_published=True),
        source='product',
        write_only=True
        )

    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'product',
            'product_id',
            'score',
            'text',
            'created_at',
            'likes_count',
            'dislikes_count',
            'user_reaction',
            'comments'
            ]


class ReactionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Reaction
        fields = ['id', 'author', 'review', 'like']


# class FlavorSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Flavor
#         fields = ['id', 'name']


# class BrandNamesSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Brand
#         fields = ['id', 'name']


# class NicotineSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Nicotine
#         fields = ['id', 'amount']
