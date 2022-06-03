from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication

from products.models import Product
from products.serializers import ProductSerializer


class AdminView(generics.ListAPIView):
    authentication_classes = TokenAuthentication
    permission_classes = IsAdminUser
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_published=False)