from rest_framework.generics import RetrieveAPIView, ListAPIView

from .serializers import ProductSerializer, BrandSerializer
from .models import Product, Brand


class ProductDetail(RetrieveAPIView):
    queryset = Product.published_objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'product_slug'


class BrandDetail(RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'brand_slug'


# class ProductList(ListAPIView):
#     queryset = Product.published_objects.all()
#     serializer_class = ProductSerializer
