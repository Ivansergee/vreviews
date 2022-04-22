from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer, BrandSerializer, ReviewSerializer
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
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class UpdateReview(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    lookup_url_kwarg = 'id'


class DeleteReview(generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Review.objects.all()
    lookup_url_kwarg = 'id'
