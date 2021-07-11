from django.contrib import admin
from .models import Item, OrderItem, Order, Sale

# Register your models here.


class SpareAdmin(admin.ModelAdmin):
    list_display = (
        'item_name', 'price', 'image', 'description', 'capacity', 'car'
    )


admin.site.register(Item, SpareAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'item', 'quantity', 'ordered'
    )


admin.site.register(OrderItem, OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user',  'ordered_date', 'ordered'
    )


admin.site.register(Order, OrderAdmin)


class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'sales_date', 'amount'
    )


admin.site.register(Sale, SaleAdmin)
