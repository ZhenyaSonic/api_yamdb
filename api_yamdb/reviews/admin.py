from django.contrib import admin

from .models import User, Category, Title, Review


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'description',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'user_id',
        'text',
        'rating',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
