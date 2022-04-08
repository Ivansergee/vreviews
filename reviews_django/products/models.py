from django.db import models
from django.contrib.auth.models import User


class Reaction(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField()  # True = like, False = dislike

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(Comment, related_name='comments')

class Producer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, db_index=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=100)
    producer = models.ForeignKey(Producer, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True, db_index=True)

    def __str__(self):
        return self.name

class Flavor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):

    class PublishedObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_published=True)

    name = models.CharField('Название', max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(blank=True)
    flavors = models.ManyToManyField(Flavor)
    slug = models.SlugField(blank=True, db_index=True)
    objects = models.Manager()
    published_objects = PublishedObjects()

    def __str__(self):
        return f'{self.brand} {self.name}'
    
    class Meta:
        ordering = ['-created_at']
