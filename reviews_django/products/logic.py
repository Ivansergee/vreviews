from products.models import Review, Product, Brand
from django.db.models import Avg, Sum


def set_product_rating(product):
    avg_score = Review.objects.filter(product=product).aggregate(avg_score=Avg('score')).get('avg_score')
    score_count = Review.objects.filter(product=product).count()
    reviews_count = Review.objects.filter(product=product).exclude(text='').count()
    product.avg_score = avg_score if avg_score else 0
    product.score_count = score_count
    product.reviews_count = reviews_count
    product.save()

def set_brand_rating(brand):
    score_count = Product.objects.filter(brand=brand).aggregate(score_count=Sum('score_count')).get('score_count')
    reviews_count = Product.objects.filter(brand=brand).aggregate(reviews_count=Sum('reviews_count')).get('reviews_count')
    if score_count:
        avg_score = Product.objects.filter(brand=brand, avg_score__gt=0).aggregate(avg_score=Avg('avg_score')).get('avg_score')
    else:
        avg_score = 0
    brand.avg_score = avg_score
    brand.score_count = score_count
    brand.reviews_count = reviews_count
    brand.save()

def set_producer_rating(producer):
    avg_score = Brand.objects.filter(producer=producer).aggregate(avg_score=Avg('avg_score')).get('avg_score')
    score_count = Brand.objects.filter(producer=producer).aggregate(score_count=Sum('score_count')).get('score_count')
    reviews_count = Brand.objects.filter(producer=producer).aggregate(reviews_count=Sum('reviews_count')).get('reviews_count')
    producer.avg_score = avg_score
    producer.score_count = score_count
    producer.reviews_count = reviews_count
    producer.save()