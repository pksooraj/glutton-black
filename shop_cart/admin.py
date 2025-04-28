from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'quantity', 'user', 'created_at', 'total_price')
    list_filter = ('size', 'created_at')
    search_fields = ('product__name', 'user__username', 'user__email')
    readonly_fields = ('total_price',)
    fieldsets = (
        ('Product Information', {
            'fields': ('product', 'size', 'quantity')
        }),
        ('User Information', {
            'fields': ('user', 'session_id')
        }),
        ('Order Details', {
            'fields': ('total_price', 'created_at', 'updated_at')
        }),
    )
    
    def total_price(self, obj):
        return f"₹{obj.total_price:.2f}"
    
    total_price.short_description = 'Total Price'
