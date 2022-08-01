from rest_framework import serializers
from django.contrib.auth.models import User
from djoser.serializers import UserSerializer

from .models import Product, Brand, Producer, Review, Comment, Reaction, Flavor, Nicotine, Profile, Bookmark


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
    flavors = serializers.StringRelatedField(many=True, read_only=True)
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
    image_url = serializers.SerializerMethodField()
    user_bookmark = serializers.SerializerMethodField()
    avg_score = serializers.FloatField(read_only=True)

    def get_image_url(self, obj):
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url)

    def get_user_bookmark(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.bookmarks.filter(author=self.context['request'].user).exists()
        return None

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
            'image_url',
            'user_bookmark',
            'avg_score',

            'get_reviews_amount',
            'get_score_amount'
        ]
        read_only_fields = ['slug']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
           self.fields.pop('image')


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

    class ProductInfo(serializers.ModelSerializer):
        image_url = serializers.SerializerMethodField()

        def get_image_url(self, obj):
            request = self.context.get('request')
            url = obj.image.url
            return request.build_absolute_uri(url)

        class Meta:
            model = Product
            fields = ['name', 'slug', 'image_url']
            read_only_fields = ['name', 'slug']


    author = serializers.StringRelatedField()
    product = ProductInfo(read_only=True)
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


class FlavorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flavor
        fields = ['id', 'name']


class BrandNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'name']


class NicotineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nicotine
        fields = ['id', 'amount']


class CustomUserSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = (
            'id',
            'email',
            'username',
            'is_staff',
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['about', 'avatar', 'birthday', 'vk', 'yt', 'tg']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']


class BookmarkSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Bookmark
        fields = ['id', 'product', 'created_at', 'author']
