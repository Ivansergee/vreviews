from django.contrib import admin
from .models import Product, Brand, Producer, Flavor


admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Producer)
admin.site.register(Flavor)
