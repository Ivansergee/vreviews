from django.contrib import admin
from .models import Product, Brand, Producer, Flavor, Review, Reaction, Comment, Nicotine, Profile, Bookmark, Volume, Country, Suggestion


class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Producer)
admin.site.register(Country)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Reaction)
admin.site.register(Comment)
admin.site.register(Flavor)
admin.site.register(Nicotine)
admin.site.register(Profile)
admin.site.register(Bookmark)
admin.site.register(Volume)
admin.site.register(Suggestion)


