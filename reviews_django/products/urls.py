from django.urls import path

from .views import ProductDetail, BrandDetail, CreateReview, UpdateReview, DeleteReview, ListReviews


urlpatterns = [
    # path('products/', ProductsList.as_view(), name='top_products'),
    path('products/<str:brand_slug>/', BrandDetail.as_view(), name='brand_detail'),
    path('products/<str:brand_slug>/<str:product_slug>/', ProductDetail.as_view(), name='product_detail'),

    path('reviews/<str:product_slug>/', ListReviews.as_view(), name='product_reviews'),
    path('reviews/create/', CreateReview.as_view(), name='create_review'),
    path('reviews/<int:id>/edit/', UpdateReview.as_view(), name='edit_review'),
    path('reviews/<int:id>/delete/', DeleteReview.as_view(), name='delete_review'),
    
    path('reviews/<int:id>/comment/', DeleteReview.as_view(), name='comment_review'),
    path('reviews/<int:id>/rate/', DeleteReview.as_view(), name='rate_review'),
    path('comment/<int:id>/rate/', DeleteReview.as_view(), name='rate_comment'),

]
