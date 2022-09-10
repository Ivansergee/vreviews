from datetime import timedelta

from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.exceptions import APIException

from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Count, Case, When
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

from .serializers import (
    ProductSerializer, BrandSerializer, ProducerSerializer, ReviewSerializer,
    CommentSerializer, ReactionSerializer, FlavorsSerializer, NicotineSerializer,
    BrandNamesSerializer, UserSerializer, ProfileSerializer, BookmarkSerializer, VolumeSerializer,
    EmailSerializer)
from .models import Product, Brand, Producer, Review, Reaction, Flavor, Nicotine, Bookmark, Profile, Volume
from .permissions import IsAuthorOrReadOnly, IsOwnerOrReadOnly, IsOwner, AuthorCanDelete
from .filters import ProductFilter, ReviewFilter
from .pagination import CustomPagination


class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_published=True) \
            .select_related('brand', 'brand__producer') \
            .prefetch_related('flavors', 'nic_content')
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    ordering_fields = ['avg_score', 'bookmarks__created_at']
    search_fields = ['name']
    pagination_class = CustomPagination


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_published=True) \
            .select_related('brand', 'brand__producer') \
            .prefetch_related('flavors', 'nic_content')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class BrandList(generics.ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.select_related('producer')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['producer__slug']
    search_fields = ['name']
    pagination_class = CustomPagination


class BrandDetail(generics.RetrieveAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.select_related('producer')
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class ProducerList(generics.ListAPIView):
    serializer_class = ProducerSerializer
    queryset = Producer.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['name']
    pagination_class = CustomPagination


class ProducerDetail(generics.RetrieveAPIView):
    serializer_class = ProducerSerializer
    queryset = Producer.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class ReviewListCreate(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter
    pagination_class = CustomPagination
    queryset = Review.objects.all()\
            .annotate(likes_count=Count(Case(When(reactions__like=True, then=1)))) \
            .annotate(dislikes_count=Count(Case(When(reactions__like=False, then=1)))) \
            .prefetch_related('comments__author') \
            .select_related('author', 'product') \
            .only(
                'score',
                'text',
                'created_at',
                'author__username',
                'product__name',
                'product__slug',
                'product__image')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewUpdate(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'
    queryset = Review.objects.all()
    lookup_url_kwarg = 'id'

    # def perform_update(self, serializer):
    #     obj = self.get_object()
    #     text = self.request.data.get('text')
    #     if text and obj.text and obj.text != text:
    #         created_at = obj.created_at
    #         delta = timedelta(minutes=30)
    #         now = timezone.now()
    #         if created_at + delta < now:
    #             raise APIException('Редактирование отзыва доступно только в течении 30 минут после создания')
    #     serializer.save()


class ReviewDelete(generics.DestroyAPIView):
    permission_classes = [AuthorCanDelete]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'


class CommentCreate(generics.CreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=Review.objects.get(pk=self.kwargs['id']))


class ReactionView(mixins.CreateModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, generics.GenericAPIView):

    serializer_class = ReactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Reaction.objects.filter(review=self.kwargs['id'])
        return queryset
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, author=self.request.user)
        return obj
    
    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=Review.objects.get(pk=self.kwargs['id']))
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ProductOptions(generics.GenericAPIView):

    def get(self, request):
        qs = Flavor.objects.order_by('name')
        flavors = FlavorsSerializer(qs, many=True).data
        qs = Brand.objects.order_by('name')
        brands = BrandNamesSerializer(qs, many=True).data
        qs = Nicotine.objects.all()
        nic_content = NicotineSerializer(qs, many=True).data
        qs = Volume.objects.all()
        volumes = VolumeSerializer(qs, many=True).data
        return Response({
            'brands': brands,
            'flavors': flavors,
            'nic_content': nic_content,
            'volumes': volumes,
            })


class FlavorCreate(generics.CreateAPIView):
    serializer_class = FlavorsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = 'username'


class EditUserProfile(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        lookup_field = self.kwargs["username"]
        return get_object_or_404(Profile, user__username=lookup_field)


class EditEmail(generics.UpdateAPIView):
    serializer_class = EmailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'
    queryset = User.objects.all()


class BookmarkView(mixins.CreateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

    serializer_class = BookmarkSerializer
    queryset = Bookmark.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, AuthorCanDelete]
    
    def get_object(self):
        queryset = self.get_queryset()
        author=self.request.user
        product=self.request.data.get('product')
        obj = get_object_or_404(queryset, author=author, product=product)
        return obj
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
