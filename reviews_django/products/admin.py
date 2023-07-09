from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Product, Brand, Producer, Flavor, Review, Reaction, Comment, Nicotine, Profile, Bookmark, Volume, Country, Suggestion, Device


class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined')


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
admin.site.register(Device)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


