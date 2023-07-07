from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from slugify import slugify


User._meta.get_field('email')._unique = True


class Country(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Flavor(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Nicotine(models.Model):
    amount = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.amount


class Volume(models.Model):
    volume = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.volume) + ' мл'


class Device(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, related_name='devices', on_delete=models.CASCADE)


class Producer(models.Model):

    def image_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'producers/img/{instance.name}.{ext}'
    
    def thumbnail_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'producers/thumb/{instance.name}.{ext}'

    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey(Country, related_name='producers', on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=image_path, default='placeholder.jpg')
    thumbnail = models.ImageField(upload_to=thumbnail_path, default='placeholder.jpg')
    slug = models.SlugField(blank=True, unique=True, db_index=True)
    website = models.URLField(null=True, blank=True)
    tg = models.URLField(null=True, blank=True)
    vk = models.URLField(null=True, blank=True)
    ig = models.URLField(null=True, blank=True)
    avg_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=None)
    score_count = models.IntegerField(null=True, blank=True, default=None)
    reviews_count = models.IntegerField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        slug_str = self.name
        self.slug = slugify(slug_str.replace("'", ""))
        super().save(*args, **kwargs)
    
    def delete(self):
        if self.image.name != 'placeholder.jpg':
            self.image.delete()
        if self.thumbnail.name != 'placeholder.jpg':
            self.thumbnail.delete()
        super().delete()
    
    class Meta:
        ordering = ['id']


class Brand(models.Model):

    def image_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'brands/img/{instance.name}.{ext}'
    
    def thumbnail_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'brands/thumb/{instance.name}.{ext}'

    name = models.CharField(max_length=100, unique=True)
    producer = models.ForeignKey(Producer, related_name='brands', on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    nic_content = models.ManyToManyField(Nicotine, related_name='brands', blank=True)
    volume = models.ManyToManyField(Volume, related_name='brands', blank=True)
    vg = models.IntegerField()
    is_salt = models.BooleanField(default=True)
    image = models.ImageField(upload_to=image_path, default='placeholder.jpg')
    thumbnail = models.ImageField(upload_to=thumbnail_path, default='placeholder.jpg')
    slug = models.SlugField(blank=True, db_index=True, unique=True)
    avg_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=None)
    score_count = models.IntegerField(null=True, blank=True, default=None)
    reviews_count = models.IntegerField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        slug_str = self.name
        self.slug = slugify(slug_str.replace("'", ""))
        super().save(*args, **kwargs)

    def delete(self):
        if self.image.name != 'placeholder.jpg':
            self.image.delete()
        if self.thumbnail.name != 'placeholder.jpg':
            self.thumbnail.delete()
        super().delete()

    class Meta:
        ordering = ['id']


class Product(models.Model):

    def image_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'products/img/{instance.brand}/{instance.name}.{ext}'
    
    def thumbnail_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'products/thumb/{instance.brand}/{instance.name}.{ext}'


    name = models.CharField('Название', max_length=100)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    nic_content = models.ManyToManyField(Nicotine, related_name='products')
    volume = models.ManyToManyField(Volume, related_name='products')
    vg = models.IntegerField()
    image = models.ImageField(upload_to=image_path, default='placeholder.jpg')
    thumbnail = models.ImageField(upload_to=thumbnail_path, default='placeholder.jpg')
    flavors = models.ManyToManyField(Flavor, related_name='products')
    slug = models.SlugField(db_index=True, unique=True, blank=True)
    is_published = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
    avg_score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=None)
    score_count = models.IntegerField(null=True, blank=True, default=None)
    reviews_count = models.IntegerField(null=True, blank=True, default=None)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.brand} {self.name}'
    
    def save(self, *args, **kwargs):
        slug_str = self.brand.name + ' ' + self.name
        self.slug = slugify(slug_str.replace("'", ""))
        super().save(*args, **kwargs)

    def delete(self):
        if self.image.name != 'placeholder.jpg':
            self.image.delete()
        if self.thumbnail.name != 'placeholder.jpg':
            self.thumbnail.delete()
        super().delete()


class Review(models.Model):
    author = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=0)
    text = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    devices = models.ManyToManyField(Device)

    def __str__(self):
        return f"{self.product} {self.author}'s review"
    
    def save(self, *args, **kwargs):
        from products.logic import set_product_rating, set_brand_rating, set_producer_rating

        super().save()
        set_product_rating(self.product)
        set_brand_rating(self.product.brand)
        set_producer_rating(self.product.brand.producer)
    

    def delete(self, *args, **kwargs):
        from products.logic import set_product_rating, set_brand_rating, set_producer_rating

        super().delete()
        set_product_rating(self.product)
        set_brand_rating(self.product.brand)
        set_producer_rating(self.product.brand.producer)
        

    class Meta:
        constraints = [models.UniqueConstraint(fields=['author', 'product'], name='unique_review')]
        ordering = ['id']


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


class Bookmark(models.Model):
    author = models.ForeignKey(User, related_name='bookmarks', on_delete=models.CASCADE, blank=False)
    product = models.ForeignKey(Product, related_name='bookmarks', on_delete=models.CASCADE, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product} bookmark by {self.author}'
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['author', 'product'], name='unique_bookmark')]


class Profile(models.Model):
    def image_path(instance, filename):
        ext = filename.split('.')[-1]
        return f'avatars/{instance.user.username}.{ext}'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to=image_path, default='default_avatar.png')
    vk = models.CharField(max_length=100, blank=True, null=True)
    yt = models.CharField(max_length=200, blank=True, null=True)
    tg = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user} profile'

    def delete(self):
        if self.avatar.name != 'default_avatar.png':
            self.avatar.delete()
        super().delete()


class Suggestion(models.Model):
    name = models.CharField('Название', max_length=100)
    comment = models.TextField(blank=True, null=True)
    author = models.ForeignKey(User, related_name='suggestion', on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    product_slug = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['processed', '-created_at']

    def __str__(self):
        return f"{self.author}'s suggestion"