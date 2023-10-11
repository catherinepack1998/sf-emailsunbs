from django.contrib import admin
from .models import Author, Category, CategorySubscription, Post, PostCategory, Comment

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(CategorySubscription)
