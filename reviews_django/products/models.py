from django.db import models
from django.db.models import Avg, Count, Sum, F
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.conf import settings


class Producer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, db_index=True)

    def __str__(self):
        return self.name


class Brand(models.Model):

    def image_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'brands/{instance.name}.{ext}'

    name = models.CharField(max_length=100, unique=True)
    producer = models.ForeignKey(Producer, related_name='brands', on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='brands/', default='placeholder.jpg')
    slug = models.SlugField(blank=True, db_index=True, unique=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return settings.HOST_URL + self.image.url
        else:
            return ''

    
    def get_avg_score(self):
        p = Product.published_objects.filter(brand__slug=self.slug)
        avg = p.annotate(avg_score=Avg('reviews__score')).aggregate(
            avg_score_brand=Avg(F('avg_score')))['avg_score_brand']
        return round(avg, 1) if avg else 0

    def get_reviews_amount(self):
        p = Product.published_objects.filter(brand__slug=self.slug)
        n = p.annotate(rev_amount=Count('reviews')).aggregate(
            rev_amount_brand=Sum(F('rev_amount')))['rev_amount_brand']
        return n

    def get_score_amount(self):
        p = Product.published_objects.filter(brand__slug=self.slug)
        n = p.annotate(score_amount=Count('reviews__score')).aggregate(
            score_amount_brand=Sum(F('score_amount')))['score_amount_brand']
        return n


class Flavor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Nicotine(models.Model):
    amount = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.amount


class Product(models.Model):

    class PublishedObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_published=True)

    
    def image_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'products/{instance.brand}/{instance.name}.{ext}'


    name = models.CharField('Название', max_length=100)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    nic_content = models.ManyToManyField(Nicotine, related_name='products')
    is_salt = models.BooleanField()
    image = models.ImageField(upload_to=image_path, default='placeholder.jpg')
    flavors = models.ManyToManyField(Flavor, related_name='products')
    slug = models.SlugField(blank=True, db_index=True, unique=True)
    is_published = models.BooleanField(default=False)
    objects = models.Manager()
    published_objects = PublishedObjects()
    
    class Meta:
        ordering = ['-created_at']
        default_manager_name = 'published_objects'

    
    def __str__(self):
        return f'{self.brand} {self.name}'
    
    def get_absolute_url(self):
        return f'/{self.brand.slug}/{self.slug}/'
    
    def get_image(self):
        return settings.HOST_URL + self.image.url
    
    def get_avg_score(self):
        p = Product.published_objects.get(slug=self.slug)
        avg_score = p.reviews.all().aggregate(Avg('score'))['score__avg']
        return round(avg_score, 1) if avg_score else 0

    def get_reviews_amount(self):
        p = Product.published_objects.get(slug=self.slug)
        return p.reviews.exclude(text__exact='').count()

    def get_score_amount(self):
        p = Product.published_objects.get(slug=self.slug)
        return p.reviews.all().count()


class Review(models.Model):
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, blank=False)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, blank=False)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=False, default=0)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} {self.author}'s review"

    def likes_count(self):
        return Reaction.objects.filter(review=self.pk).filter(like=True).count()

    def dislikes_count(self):
        return Reaction.objects.filter(review=self.pk).filter(like=False).count()

    class Meta:
        constraints = [models.UniqueConstraint(fields=['author', 'product'], name='unique_review')]


class Comment(models.Model):
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, blank=False)
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE, blank=False)
    text = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.review} comment'


class Reaction(models.Model):
    author = models.ForeignKey(User, related_name='reactions', on_delete=models.CASCADE, blank=False)
    review = models.ForeignKey(Review, related_name='reactions', on_delete=models.CASCADE, blank=False)
    like = models.BooleanField()  # True = like, False = dislike

    def __str__(self):
        return f'{self.review}' + (' like' if self.like else ' dislike') + f' by {self.author}'
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['author', 'review'], name='unique_reaction')]
