from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser

from django_filters.rest_framework import DjangoFilterBackend

from django.db.models import Avg, OuterRef, Subquery
from django.shortcuts import get_object_or_404

# from .serializers import (
#     NicotineSerializer, FlavorSerializer, CreateProductSerializer, BrandNameSerializer,
#     ProductSerializer, BrandDetailSerializer, ReviewSerializer, ProductReviewSerializer,
#     CommentSerializer, ReactionSerializer)
from .serializers import ProductSerializer, BrandSerializer, ProducerSerializer, ReviewSerializer, CommentSerializer, ReactionSerializer
from .models import Product, Brand, Producer, Review, Reaction, Flavor, Nicotine
from .permissions import IsAuthorOrReadOnly


class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['brand__slug']

    def get_queryset(self):
        if self.request.method == 'GET':
            return Product.objects.filter(is_published=True)
        if self.request.method == 'POST':
            return Product.objects.all()


class ProductDetail(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_published=True)
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
    filterset_fields = ['product__slug', 'author__username']

    def get_queryset(self):
        if self.request.method == 'GET':
            if self.request.user.is_authenticated:
                user_reactions = Reaction.objects.filter(review=OuterRef('pk'), author=self.request.user)
                queryset = Review.objects.annotate(user_reaction=Subquery(user_reactions.values('like')[:1]))
                return queryset
            return Review.objects.all()
        return Review.objects.all()
    
    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class ReviewUpdate(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()


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


# class FlavorsListCreate(generics.ListCreateAPIView):
#     serializer_class = FlavorSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     authentication_classes = [TokenAuthentication]
#     queryset = Flavor.objects.order_by('name')


# class NicotineList(generics.ListAPIView):
#     serializer_class = NicotineSerializer
#     queryset = Nicotine.objects.all()
