from django_filters import rest_framework as filters

from .models import Product, Review


class ProductFilter(filters.FilterSet):
    brand = filters.CharFilter(field_name='brand__slug')
    bookmarks_author = filters.CharFilter(field_name='bookmarks__author__username')

    class Meta:
        model = Product
        fields = ['brand__slug', 'bookmarks__author__username']


class ReviewFilter(filters.FilterSet):
    product = filters.CharFilter(field_name='product__slug')
    author = filters.CharFilter(field_name='author__username')

    class Meta:
        model = Review
        fields = ['product__slug', 'author__username']