from django.contrib import admin
from .models import Product, Category, CategoryProduct, Review


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(CategoryProduct)
admin.site.register(Review)