from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product', 'custom_design']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'email', 'status_display', 'total_items', 'created_at', 'actions_display']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['first_name', 'last_name', 'email', 'id']
    inlines = [OrderItemInline]
    readonly_fields = ['created_at', 'updated_at', 'order_summary']
    date_hierarchy = 'created_at'
    list_per_page = 20
    actions = ['mark_as_processing', 'mark_as_shipped', 'mark_as_delivered', 'mark_as_cancelled']
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Details', {
            'fields': ('address', 'city', 'state', 'zipcode', 'country')
        }),
        ('Order Status', {
            'fields': ('status',),
            'classes': ('wide',)
        }),
        ('Order Details', {
            'fields': ('created_at', 'updated_at', 'order_summary'),
            'classes': ('collapse',)
        }),
    )
    
    def customer_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    customer_name.short_description = 'Customer'
    
    def total_items(self, obj):
        return obj.items.count()
    total_items.short_description = 'Items'
    
    def order_summary(self, obj):
        items = obj.items.all()
        html = '<div style="padding: 10px; background-color: #f9f9f9; border-radius: 4px;">'
        for item in items:
            html += f'<p><strong>{item.product.name}</strong> - Quantity: {item.quantity}</p>'
        html += '</div>'
        return format_html(html)
    order_summary.short_description = 'Order Summary'
    
    def status_display(self, obj):
        status_classes = {
            'pending': 'status-pending',
            'processing': 'status-processing',
            'shipped': 'status-shipped',
            'delivered': 'status-delivered',
            'cancelled': 'status-cancelled'
        }
        status_class = status_classes.get(obj.status, '')
        return format_html('<span class="order-status {}">{}</span>', status_class, obj.get_status_display())
    status_display.short_description = 'Status'
    
    def actions_display(self, obj):
        actions = ''
        if obj.status == 'pending':
            actions += format_html('<a class="button" style="background-color: #3B82F6; color: white; margin-right: 5px;" href="#">Process</a>')
        elif obj.status == 'processing':
            actions += format_html('<a class="button" style="background-color: #10B981; color: white; margin-right: 5px;" href="#">Ship</a>')
        elif obj.status == 'shipped':
            actions += format_html('<a class="button" style="background-color: #059669; color: white; margin-right: 5px;" href="#">Deliver</a>')
        
        return actions
    actions_display.short_description = 'Quick Actions'
    
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')
    mark_as_processing.short_description = 'Mark as Processing'
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = 'Mark as Shipped'
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = 'Mark as Delivered'
    
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_as_cancelled.short_description = 'Mark as Cancelled'
