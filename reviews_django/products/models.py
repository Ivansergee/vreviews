from django.db import models
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
    name = models.CharField(max_length=100, unique=True)
    producer = models.ForeignKey(Producer, related_name='brands', on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='brands/', default='placeholder.jpg')
    slug = models.SlugField(blank=True, db_index=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return settings.HOST_URL + self.image.url
        else:
            return ''

class Flavor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):

    class PublishedObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_published=True)

    name = models.CharField('Название', max_length=100)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', default='placeholder.jpg')
    flavors = models.ManyToManyField(Flavor, related_name='products')
    slug = models.SlugField(blank=True, db_index=True)
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
        if self.image:
            return settings.HOST_URL + self.image.url
        else:
            return ''
    
    def get_avg_score(self):
        p = Product.published_objects.get(slug=self.slug)
        avg_score = p.reviews.all().aggregate(models.Avg('score'))['score__avg']
        return round(avg_score, 1)

    def get_reviews_amount(self):
        p = Product.published_objects.get(slug=self.slug)
        return p.reviews.exclude(text__exact='').count()

    def get_score_amount(self):
        p = Product.published_objects.get(slug=self.slug)
        return p.reviews.all().count()


class Review(models.Model):
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE, blank=False)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, blank=False)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], blank=False)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product} {self.author}'s review"

    def get_total_likes(self):
        pass
    
    def get_total_dislikes(self):
        pass

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

