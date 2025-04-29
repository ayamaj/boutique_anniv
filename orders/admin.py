from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email',
                   'total_price', 'payment_status', 'created', 'updated']
    list_filter = ['payment_status', 'created', 'updated']
    search_fields = ['first_name', 'last_name', 'email', 'address', 'city']
    inlines = [OrderItemInline]
    readonly_fields = ['created', 'updated', 'total_price']
    fieldsets = (
        (None, {
            'fields': ('user', 'payment_status', 'stripe_payment_intent')
        }),
        ('Informations client', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Adresse', {
            'fields': ('address', 'postal_code', 'city')
        }),
        ('Dates et prix', {
            'fields': ('total_price', 'created', 'updated')
        }),
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']
    list_filter = ['order__payment_status']
    search_fields = ['product__name', 'order__id']