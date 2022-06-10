from django.urls import path

# from .views import (
#     FlavorsListCreate, ProductCreate, ProductList, ProductDetail,
#     BrandsList, BrandDetail, CreateReview, UpdateReview, DeleteReview,
#     ListReviews, CreateComment, CreateReaction, UpdateDeleteReaction,
#     NicotineList)
from .views import ProductListCreate, ProductDetail, BrandList, BrandDetail



urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='products'),
    path('products/<str:slug>', ProductDetail.as_view(), name='product_detail'),

    path('brands/', BrandList.as_view(), name='brands'),
    path('brands/<str:slug>', BrandDetail.as_view(), name='brand_detail'),
    # path('products/<str:product_slug>/reviews/', ListReviews.as_view(), name='product_reviews'),

    # path('brands/', BrandsList.as_view(), name='brands'),
    # path('brand/<str:brand_slug>/', BrandDetail.as_view(), name='brand_detail'),

    # path('flavors/', FlavorsListCreate.as_view(), name='flavors'),
    # path('nic-content/', NicotineList.as_view(), name='nic-content'),

    # path('review/create/', CreateReview.as_view(), name='create_review'),
    # path('review/<int:id>/edit/', UpdateReview.as_view(), name='edit_review'),
    # path('review/<int:id>/delete/', DeleteReview.as_view(), name='delete_review'),
    # path('review/<int:id>/comment/', CreateComment.as_view(), name='create_comment'),
    # path('review/<int:id>/rate/', CreateReaction.as_view(), name='rate_review'),
    # path('review/<int:id>/edit-reaction/', UpdateDeleteReaction.as_view(), name='edit_reaction'),
]
