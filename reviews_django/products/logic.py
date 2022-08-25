from products.models import Review
from django.db.models import Avg


def set_product_rating(product):
    avg_score = Review.objects.filter(product=product).aggregate(avg_score=Avg('score')).get('avg_score')
    score_count = Review.objects.filter(product=product).count()
    reviews_count = Review.objects.filter(product=product).exclude(text='').count()
    product.avg_score = avg_score
    product.score_count = score_count
    product.reviews_count = reviews_count
    product.save()