from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser

from django.db.models import Avg, OuterRef, Subquery
from django.shortcuts import get_object_or_404

from .serializers import (
    NicotineSerializer, FlavorSerializer, CreateProductSerializer, BrandNameSerializer,
    ProductSerializer, BrandDetailSerializer, ReviewSerializer, ProductReviewSerializer,
    CommentSerializer, ReactionSerializer)
from .models import Product, Brand, Review, Reaction, Flavor, Nicotine


class ProductCreate(generics.CreateAPIView):
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]


class FlavorsListCreate(generics.ListCreateAPIView):
    serializer_class = FlavorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]
    queryset = Flavor.objects.order_by('name')


class NicotineList(generics.ListAPIView):
    serializer_class = NicotineSerializer
    queryset = Nicotine.objects.all()


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.published_objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'product_slug'


class ProductList(generics.ListAPIView):
    queryset = Product.published_objects.annotate(avg_score=Avg('reviews__score')).order_by('-avg_score')
    serializer_class = ProductSerializer


class BrandsList(generics.ListAPIView):
    queryset = Brand.objects.order_by('name')
    serializer_class = BrandNameSerializer


class BrandDetail(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'brand_slug'


class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class UpdateReview(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    lookup_url_kwarg = 'id'


class DeleteReview(generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    lookup_url_kwarg = 'id'


class ListReviews(generics.ListAPIView):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        if self.request.user.is_authenticated:
            user_reactions = Reaction.objects.filter(review=OuterRef('pk'), author=self.request.user)
            queryset = Review.objects.filter(product__slug=product_slug).annotate(user_reaction=Subquery(user_reactions.values('like')[:1]))
        else:
            queryset = Review.objects.filter(product__slug=product_slug)
        return queryset


class CreateComment(generics.CreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CreateReaction(generics.CreateAPIView):
    serializer_class = ReactionSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=Review.objects.get(pk=self.kwargs['id'])
            )


class UpdateDeleteReaction(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
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

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

