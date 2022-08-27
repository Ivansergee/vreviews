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
    volume = serializers.StringRelatedField(many=True)
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
            'short_desc',
            'description',
            'slug',
            'brand',
            'brand_id',
            'vg',
            'volume',
            'flavors',
            'flavor_id',
            'nic_content',
            'nic_content_id',
            'is_salt',
            'image',
            'image_url',
            'user_bookmark',
            'avg_score',
            'reviews_count',
            'score_count',
        ]
        read_only_fields = ['slug', 'avg_score', 'reviews_count', 'score_count']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
           self.fields.pop('image')


class BrandSerializer(serializers.ModelSerializer):
    producer = ProducerShortSerializer(read_only=True)
    avg_score = serializers.DecimalField(max_digits=None, decimal_places=2, read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    score_count = serializers.IntegerField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'producer',
            'image',
            'image_url',

            'avg_score',
            'reviews_count',
            'score_count',
        ]
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
           self.fields.pop('image')


class ProducerSerializer(serializers.ModelSerializer):
    avg_score = serializers.DecimalField(max_digits=None, decimal_places=2, read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    score_count = serializers.IntegerField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'image',
            'image_url',

            'avg_score',
            'reviews_count',
            'score_count',
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
           self.fields.pop('image')


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
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    user_reaction = serializers.SerializerMethodField()
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_published=True),
        source='product',
        write_only=True
        )
    
    def get_user_reaction(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            qs = Reaction.objects.filter(author=user, review=obj.id)
            if qs:
                return qs[0].like
        return None

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.context['request'].user.is_authenticated:
           self.fields.pop('user_reaction')

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
        fields = ['about', 'avatar', 'city', 'birthday', 'vk', 'yt', 'tg']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']
        read_only_fields = ['username']
    
    def update(self, instance, validated_data):
        if 'profile' in validated_data:
            nested_serializer = self.fields['profile']
            nested_instance = instance.profile
            nested_data = validated_data.pop('profile')
            nested_serializer.update(nested_instance, nested_data)

        return super().update(instance, validated_data)


class BookmarkSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Bookmark
        fields = ['id', 'product', 'created_at', 'author']
