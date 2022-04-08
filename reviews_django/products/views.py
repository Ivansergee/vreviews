from rest_framework.generics import RetrieveAPIView

from .serializers import ProductSerializer
from .models import Product


class ProductDetail(RetrieveAPIView):
    queryset = Product.published_objects.all()
    serializer_class = ProductSerializer