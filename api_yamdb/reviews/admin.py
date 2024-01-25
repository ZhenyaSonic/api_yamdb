from django.contrib import admin

from .models import Category, Title, Review, Comment


# class UserAdmin(admin.ModelAdmin):
#     list_display = (
#         'username',
#         'email',
#         'first_name',
#         'last_name',
#     )


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
        'rating',
    )


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'text',
        'score',
        'pub_date',
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )


admin.site.register(Category, CategoryAdmin)
# admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
