import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','reviews_django.settings')

import django
django.setup()

import random
from products.models import *

for i in range(1, 6):
    Flavor.objects.create(name=f'flavor{i}')
    Nicotine.objects.create(amount=f'{i}')

for i in range(1, 12):
    Producer.objects.create(
        name=f'producer{i}',
        country=f'country{i}',
        description=f'producer{i} description',
        slug=f'producer-{i}'
    )

for producer in Producer.objects.all():
    for i in range(1, 12):
        Brand.objects.create(
            name=f'{producer} brand{i}',
            description=f"{producer}'s brand{i} description",
            slug=f'{producer}-brand-{i}',
            producer=producer
        )

for brand in Brand.objects.all():
    for i in range(1, 12):
        product = Product.objects.create(
            name=f'{brand} product{i}',
            description=f"{brand}'s product{i} description",
            is_salt=bool(random.randint(0, 1)),
            slug=f'{brand}-product-{i}',
            is_published=True,
            brand=brand
        )
        product.flavors.add(
            *random.sample(
                list(Flavor.objects.all()),
                random.randint(1, 5)
                ))
        product.nic_content.add(
            *random.sample(
                list(Nicotine.objects.all()),
                random.randint(1, 5)
                ))

for i in range(1, 21):
    User.objects.create_user(
        username=f'user{i}',
        password='1234'
    )

for product in Product.objects.all():
    users = list(User.objects.all())
    for i in range(1, 12):
        Review.objects.create(
            author=users.pop(),
            product=product,
            score=random.randint(1, 10),
            text=f'{product} review {i}',
        )

for review in Review.objects.all():
    for i in range(1, 6):
        Comment.objects.create(
            author=random.choice(list(User.objects.all())),
            review=review,
            text=f'Comment {i} for {review}'
        )

for user in User.objects.all():
    products = random.sample(list(Product.objects.all()), 12)
    for product in products:
        Bookmark.objects.create(
            author=user,
            product=product,            
        )