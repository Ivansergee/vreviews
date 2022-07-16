from datetime import timedelta

from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import APIException

from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Avg, OuterRef, Subquery
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.utils import timezone

from .serializers import (
    ProductSerializer, BrandSerializer, ProducerSerializer, ReviewSerializer,
    CommentSerializer, ReactionSerializer, FlavorsSerializer, NicotineSerializer,
    BrandNamesSerializer, UserProfileSerializer, BookmarkSerializer)
from .models import Product, Brand, Producer, Review, Reaction, Flavor, Nicotine, Bookmark
from .permissions import IsAuthorOrReadOnly, IsOwnerOrReadOnly, AuthorCanDelete
from .filters import ProductFilter, ReviewFilter


class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_published=True).annotate(avg_score=Avg('reviews__score'))
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['avg_score', 'bookmarks__created_at']


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_published=True).annotate(avg_score=Avg('reviews__score'))
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class BrandList(generics.ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['producer__slug']


class BrandDetail(generics.RetrieveAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class ProducerList(generics.ListAPIView):
    serializer_class = ProducerSerializer
    queryset = Producer.objects.all()


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

    def get_queryset(self):
        if self.request.method == 'GET':
            if self.request.user.is_authenticated:
                user_reactions = Reaction.objects.filter(review=OuterRef('pk'), author=self.request.user)
                queryset = Review.objects.annotate(user_reaction=Subquery(user_reactions.values('like')[:1]))
                return queryset
        return Review.objects.all()
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class ReviewUpdate(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'id'
    queryset = Review.objects.all()
    lookup_url_kwarg = 'id'

    def perform_update(self, serializer):
        obj = self.get_object()
        text = self.request.data.get('text')
        if text and obj.text != text:
            created_at = obj.created_at
            delta = timedelta(minutes=30)
            now = timezone.now()
            if created_at + delta < now:
                raise APIException('Редактирование отзыва доступно только в течении 30 минут после создания')
        serializer.save()


class ReviewDelete(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
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

# class ReviewDelete(generics.DestroyAPIView):
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAdminUser]
#     authentication_classes = [TokenAuthentication]
#     queryset = Review.objects.all()
#     lookup_url_kwarg = 'id'


class FlavorsListCreate(generics.ListCreateAPIView):
    serializer_class = FlavorsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Flavor.objects.order_by('name')


class NicotineList(generics.ListAPIView):
    serializer_class = NicotineSerializer
    queryset = Nicotine.objects.all()


class BrandNames(generics.ListAPIView):
    serializer_class = BrandNamesSerializer
    queryset = Brand.objects.all()


class AdminProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand__slug', 'is_published']


class AdminProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'


class UserView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    queryset = User.objects.all()
    lookup_field = 'username'


class BookmarkView(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):

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
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
