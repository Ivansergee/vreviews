from django.urls import path

from .views import ProductDetail, BrandDetail


urlpatterns = [
    # path('products/', ProductList.as_view(), name='products_list'),
    path('products/<str:brand_slug>/', BrandDetail.as_view(), name='brand_detail'),
    path('products/<str:brand_slug>/<str:product_slug>/', ProductDetail.as_view(), name='product_detail'),
]
