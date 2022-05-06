from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.db.models import Count, Q, OuterRef, Subquery

from .serializers import ProductSerializer, BrandSerializer, ReviewSerializer, ProductReviewSerializer, CommentSerializer, ReactionSerializer
from .models import Product, Brand, Review, Reaction


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.published_objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'product_slug'


class BrandDetail(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'brand_slug'


# class ProductsList(generics.ListAPIView):
#     queryset = Product.published_objects.all()
#     serializer_class = ProductSerializer


class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class UpdateReview(generics.UpdateAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    lookup_url_kwarg = 'id'


class DeleteReview(generics.DestroyAPIView):
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Review.objects.all()
    lookup_url_kwarg = 'id'


class ListReviews(generics.ListAPIView):
    serializer_class = ProductReviewSerializer

    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        user_reactions = Reaction.objects.filter(review=OuterRef('pk'), author=self.request.user)
        queryset = Review.objects.filter(product__slug=product_slug).annotate(
                likes_count=Count('reactions', filter=Q(reactions__like=True)),
                dislikes_count=Count('reactions', filter=Q(reactions__like=False)),
                user_reaction=Subquery(user_reactions.values('like')[:1])
                )
        return queryset


class CreateComment(generics.CreateAPIView):
    serializer_class = CommentSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class CreateReaction(generics.CreateAPIView):
    serializer_class = ReactionSerializer
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=Review.objects.get(pk=self.kwargs['id'])
            )


class UpdateDeleteReaction(mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = ReactionSerializer
    authentication_classes = [TokenAuthentication]
    
    def get_queryset(self):
        queryset = Reaction.objects.filter(review=self.kwargs['id'], author=self.request.user)
        return queryset

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

