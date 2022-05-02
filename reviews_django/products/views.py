from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import ProductSerializer, BrandSerializer, ReviewSerializer, ProductReviewSerializer, CommentSerializer
from .models import Product, Brand, Review


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.published_objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'product_slug'


class BrandDetail(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'brand_slug'


# class ProductsList(generics.ListAPIView):
#     queryset = Product.published_objects.all()
#     serializer_class = ProductSerializer


class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class UpdateReview(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    lookup_url_kwarg = 'id'


class DeleteReview(generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    lookup_url_kwarg = 'id'


class ListReviews(generics.ListAPIView):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        queryset = Review.objects.filter(product__slug=product_slug)
        return queryset


class CreateComment(generics.CreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class LikeReview(generics.CreateAPIView):
    pass