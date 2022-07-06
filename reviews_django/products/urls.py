from django.urls import path

# from .views import (
#     FlavorsListCreate, ProductCreate, ProductList, ProductDetail,
#     BrandsList, BrandDetail, CreateReview, UpdateReview, DeleteReview,
#     ListReviews, CreateComment, CreateReaction, UpdateDeleteReaction,
#     NicotineList)
from .views import (ProductListCreate, ProductDetail, BrandList, BrandDetail, ProducerList,
                    ProducerDetail, ReviewListCreate, ReviewUpdate, CommentCreate, ReactionView,
                    FlavorsListCreate, NicotineList, BrandNames, UserView)



urlpatterns = [
    path('products/', ProductListCreate.as_view(), name='products'),
    path('products/<str:slug>/', ProductDetail.as_view(), name='product_detail'),

    path('brands/', BrandList.as_view(), name='brands'),
    path('brands/<str:slug>/', BrandDetail.as_view(), name='brand_detail'),

    path('producers/', ProducerList.as_view(), name='producers'),
    path('producers/<str:slug>/', ProducerDetail.as_view(), name='producer_detail'),

    path('reviews/', ReviewListCreate.as_view(), name='reviews'),
    path('reviews/<int:id>/edit/', ReviewUpdate.as_view(), name='edit_review'),
    path('reviews/<int:id>/comment/', CommentCreate.as_view(), name='create_comment'),
    path('reviews/<int:id>/rate/', ReactionView.as_view(), name='rate_review'),

    path('flavors/', FlavorsListCreate.as_view(), name='flavors'),
    path('nic-content/', NicotineList.as_view(), name='nic_contents'),
    path('brand-names/', BrandNames.as_view(), name='brand_names'),

    path('user/<str:username>/', UserView.as_view(), name='user')
]
