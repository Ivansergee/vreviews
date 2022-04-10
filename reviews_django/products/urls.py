from django.urls import path

from .views import ProductDetail, BrandProducts


urlpatterns = [
    # path('products/', ProductList.as_view(), name='products_list'),
    path('<str:brand_slug>/', BrandProducts.as_view(), name='brand_products'),
    path('<str:brand_slug>/<str:product_slug>/', ProductDetail.as_view(), name='product_detail'),
]
