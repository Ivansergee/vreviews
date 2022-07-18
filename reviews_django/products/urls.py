from django.urls import path

from .views import (ProductListCreate, ProductDetail, BrandList, BrandDetail, ProducerList,
                    ProducerDetail, ReviewListCreate, ReviewUpdate, ReviewDelete, CommentCreate, ReactionView,
                    ProductCreateOptions, UserView, BookmarkView)



urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='products'),
    path('products/<str:slug>/', ProductDetail.as_view(), name='product_detail'),

    path('brands/', BrandList.as_view(), name='brands'),
    path('brands/<str:slug>/', BrandDetail.as_view(), name='brand_detail'),

    path('producers/', ProducerList.as_view(), name='producers'),
    path('producers/<str:slug>/', ProducerDetail.as_view(), name='producer_detail'),

    path('reviews/', ReviewListCreate.as_view(), name='reviews'),
    path('reviews/<int:id>/edit/', ReviewUpdate.as_view(), name='edit_review'),
    path('reviews/<int:id>/delete/', ReviewDelete.as_view(), name='delete_review'),
    path('reviews/<int:id>/comment/', CommentCreate.as_view(), name='create_comment'),
    path('reviews/<int:id>/rate/', ReactionView.as_view(), name='rate_review'),

    path('product-options/', ProductCreateOptions.as_view(), name='product-options'),


    path('user/<str:username>/', UserView.as_view(), name='user'),

    path('bookmarks/', BookmarkView.as_view(), name='bookmark'),
]
