from django.contrib import admin
from .models import *


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'currency')
    search_fields = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id',)


class TaxAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Discount, DiscountAdmin)