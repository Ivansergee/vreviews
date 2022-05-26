from django.contrib import admin
from .models import Product, Brand, Producer, Flavor, Review, Reaction, Comment, Nicotine


class ProductAdmin(admin.ModelAdmin):
    model = Product

    def get_queryset(self, request):
        return self.model.objects.all()


admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(Producer)
admin.site.register(Review)
admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(Flavor)
admin.site.register(Nicotine)


