from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from djoser.conf import settings
from djoser.serializers import UserSerializer, TokenCreateSerializer

from .models import Product, Brand, Producer, Review, Comment, Reaction, Flavor, Nicotine, Profile, Bookmark, Volume, Country


class ProducerShortSerializer(serializers.ModelSerializer):

    country = serializers.StringRelatedField()

    class Meta:
        model = Producer
        fields = ['id','name', 'slug', 'country']


class BrandShortSerializer(serializers.ModelSerializer):
    producer = ProducerShortSerializer(read_only=True)
    nic_content = serializers.StringRelatedField(many=True)
    volume = serializers.StringRelatedField(many=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'nic_content', 'volume', 'is_salt', 'slug', 'producer']


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ['id', 'name']


class VolumeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Volume
        fields = ['id', 'volume']
        read_only_fields = ['volume']


class FlavorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flavor
        fields = ['id', 'name']


class BrandNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ['id', 'name']


class ProducerNamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producer
        fields = ['id', 'name']


class NicotineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nicotine
        fields = ['id', 'amount']


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandShortSerializer(read_only=True)
    flavors = FlavorsSerializer(many=True, read_only=True)
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
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    user_bookmark = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url)
    
    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        url = obj.thumbnail.url
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
            'vg',
            'flavors',
            'flavor_id',
            'image',
            'image_url',
            'thumbnail',
            'thumbnail_url',
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
           self.fields.pop('thumbnail')


class BrandSerializer(serializers.ModelSerializer):
    producer = ProducerShortSerializer(read_only=True)
    nic_content = NicotineSerializer(many=True, read_only=True)
    volume = VolumeSerializer(many=True, read_only=True)
    avg_score = serializers.DecimalField(max_digits=None, decimal_places=2, read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)
    score_count = serializers.IntegerField(read_only=True)
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()
    nic_content_id = serializers.PrimaryKeyRelatedField(
        queryset=Nicotine.objects.all(),
        source='nic_content',
        many=True,
        write_only=True
        )
    volume_id = serializers.PrimaryKeyRelatedField(
        queryset=Volume.objects.all(),
        source='volume',
        many=True,
        write_only=True
        )
    producer_id = serializers.PrimaryKeyRelatedField(
        queryset=Producer.objects.all(),
        source='producer',
        write_only=True
        )

    class Meta:
        model = Brand
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'volume',
            'volume_id',
            'nic_content',
            'nic_content_id',
            'is_salt',
            'producer',
            'producer_id',
            'image',
            'thumbnail',
            'image_url',
            'thumbnail_url',

            'avg_score',
            'reviews_count',
            'score_count',
        ]
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url)
    
    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        url = obj.thumbnail.url
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
    thumbnail_url = serializers.SerializerMethodField()
    country = serializers.StringRelatedField()
    country_id = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(),
        source='country',
        write_only=True
        )

    class Meta:
        model = Producer
        fields = [
            'id',
            'name',
            'description',
            'country',
            'country_id',
            'slug',
            'image',
            'thumbnail',
            'image_url',
            'thumbnail_url',
            'website',
            'tg',
            'vk',
            'ig',

            'avg_score',
            'reviews_count',
            'score_count',
        ]
        read_only_fields = ['country']

    def get_image_url(self, obj):
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url)
    
    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        url = obj.thumbnail.url
        return request.build_absolute_uri(url)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'GET':
           self.fields.pop('image')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_avatar','review', 'text', 'created_at']
        read_only_fields = ['review']
    

    def get_author_avatar(self, obj):
        request = self.context.get('request')
        url = obj.author.profile.avatar.url
        return request.build_absolute_uri(url)


class ReviewSerializer(serializers.ModelSerializer):

    class ProductInfo(serializers.ModelSerializer):
        thumbnail_url = serializers.SerializerMethodField()

        def get_thumbnail_url(self, obj):
            request = self.context.get('request')
            url = obj.thumbnail.url
            return request.build_absolute_uri(url)

        class Meta:
            model = Product
            fields = ['name', 'slug', 'thumbnail_url']


    author = serializers.StringRelatedField()
    author_avatar = serializers.SerializerMethodField()
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
    
    def get_author_avatar(self, obj):
        request = self.context.get('request')
        url = obj.author.profile.avatar.url
        return request.build_absolute_uri(url)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.context['request'].user.is_authenticated:
           self.fields.pop('user_reaction')

    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'author_avatar',
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


class EmailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']
    
    def update(self, instance, validated_data):
        if instance.check_password(validated_data.get('password')):
            validated_data.pop('password')
            instance.email = validated_data.get('email', instance.email)
            return super().update(instance, validated_data)
        raise ValidationError('Wrong password')

class BookmarkSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Bookmark
        fields = ['id', 'product', 'created_at', 'author']


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if not self.user or not self.user.check_password(password):
                self.fail("invalid_credentials")
        if not self.user.is_active:
            raise ValidationError('User is not active')
        if self.user and self.user.is_active:
            return attrs
        self.fail("invalid_credentials")


class AdminProductSerializer(serializers.ModelSerializer):
    brand = BrandShortSerializer(read_only=True)
    flavors = serializers.StringRelatedField(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    thumbnail_url = serializers.SerializerMethodField()

    def get_image_url(self, obj):
        request = self.context.get('request')
        url = obj.image.url
        return request.build_absolute_uri(url)
    
    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        url = obj.thumbnail.url
        return request.build_absolute_uri(url)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'flavors',
            'slug',
            'brand',
            'vg',
            'image_url',
            'thumbnail_url',
            'is_published'
        ]
