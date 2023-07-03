from django.urls import path

from .views import (ProductListCreate, ProductDetail, BrandListCreate, BrandDetail, ProducerListCreate,
                    ProducerDetail, ReviewListCreate, ReviewUpdate, ReviewDelete, CommentCreate, ReactionView,
                    CreateOptions, UserView, BookmarkView, EditUserProfile, EditEmail, UnpublishedProductList,
                    AdminProductDetail, BrandChoices, SuggestionListCreate, SuggestionDetail)



urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='products'),
    path('products/<str:slug>/', ProductDetail.as_view(), name='product_detail'),

    path('brands/', BrandListCreate.as_view(), name='brands'),
    path('brands/<str:slug>/', BrandDetail.as_view(), name='brand_detail'),
    path('brand-choices/<int:id>/', BrandChoices.as_view(), name='brand_choices'),

    path('producers/', ProducerListCreate.as_view(), name='producers'),
    path('producers/<str:slug>/', ProducerDetail.as_view(), name='producer_detail'),

    path('reviews/', ReviewListCreate.as_view(), name='reviews'),
    path('reviews/<int:id>/edit/', ReviewUpdate.as_view(), name='edit_review'),
    path('reviews/<int:id>/delete/', ReviewDelete.as_view(), name='delete_review'),
    path('reviews/<int:id>/comment/', CommentCreate.as_view(), name='create_comment'),
    path('reviews/<int:id>/rate/', ReactionView.as_view(), name='rate_review'),

    path('create-options/', CreateOptions.as_view(), name='product-options'),

    path('user/<str:username>/', UserView.as_view(), name='user'),
    path('user/<str:username>/edit/', EditUserProfile.as_view(), name='user_edit'),
    path('user/<str:username>/edit-email/', EditEmail.as_view(), name='edit_email'),

    path('bookmarks/', BookmarkView.as_view(), name='bookmark'),

    path('suggestions/', SuggestionListCreate.as_view(), name='suggestions'),
    path('suggestions/<int:id>/', SuggestionDetail.as_view(), name='suggestion'),

    path('admin/', UnpublishedProductList.as_view(), name='unpublished_products'),
    path('admin/<str:slug>/', AdminProductDetail.as_view(), name='admin_product_detail'),
]
