from django.contrib import admin
from .models import Product, Brand, Producer, Flavor, Review, Reaction, Comment


admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Producer)
admin.site.register(Review)
admin.site.register(Reaction)
admin.site.register(Comment)

