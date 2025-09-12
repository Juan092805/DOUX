from django.contrib import admin
from .models import Category, Product, Wishlist, Order, OrderItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active", "created_at")
    list_filter = ("category", "is_active", "gender")
    search_fields = ("name", "description")

admin.site.register(Category)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
