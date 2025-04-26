from django.contrib import admin
from .models import Product, ProductImage, WishlistItem
from django.utils.html import format_html

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_main']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return ""

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_display', 'is_featured', 'in_stock', 'image_thumbnail', 'created_at']
    list_display_links = ['name', 'image_thumbnail']
    list_filter = ['is_featured', 'in_stock', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'short_description': ('name',)}
    inlines = [ProductImageInline]
    list_per_page = 20
    save_on_top = True
    actions = ['mark_as_featured', 'mark_as_not_featured', 'mark_as_in_stock', 'mark_as_out_of_stock', 'duplicate_product']
    list_editable = ['is_featured', 'in_stock']
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'price', 'short_description', 'description'),
            'classes': ('wide', 'extrapretty'),
        }),
        ('Product Status', {
            'fields': ('is_featured', 'in_stock'),
            'description': 'Control the visibility and availability of this product',
            'classes': ('collapse',),
        }),
    )
    
    def image_thumbnail(self, obj):
        # Get the main image or first image
        image = obj.images.filter(is_main=True).first() or obj.images.first()
        if image and image.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px;" />', image.image.url)
        return format_html('<span style="color: #999;">No image</span>')
    image_thumbnail.short_description = 'Image'
    
    def price_display(self, obj):
        return f"${obj.price:.2f}"
    price_display.short_description = 'Price'
    
    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = 'Mark selected products as featured'
    
    def mark_as_in_stock(self, request, queryset):
        queryset.update(in_stock=True)
    mark_as_in_stock.short_description = 'Mark selected products as in stock'
    
    def mark_as_out_of_stock(self, request, queryset):
        queryset.update(in_stock=False)
    mark_as_out_of_stock.short_description = 'Mark selected products as out of stock'
    
    def mark_as_not_featured(self, request, queryset):
        queryset.update(is_featured=False)
    mark_as_not_featured.short_description = 'Remove selected products from featured'
    
    def duplicate_product(self, request, queryset):
        for product in queryset:
            # Create a copy of the product
            product.pk = None
            product.name = f"Copy of {product.name}"
            product.save()
            
            # Display a success message
            self.message_user(request, f"Successfully duplicated: {product.name}")
    duplicate_product.short_description = 'Duplicate selected products'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'alt_text', 'is_main', 'created_at']
    list_filter = ['is_main', 'created_at', 'product']
    search_fields = ['product__name', 'alt_text']
    readonly_fields = ['image_preview', 'image_full_preview']
    list_editable = ['is_main', 'alt_text']
    list_per_page = 20
    actions = ['mark_as_main', 'mark_as_not_main']
    
    fieldsets = (
        ('Image Information', {
            'fields': ('product', 'image', 'image_full_preview', 'alt_text'),
        }),
        ('Image Status', {
            'fields': ('is_main',),
            'description': 'Set this image as the main product image',
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px; max-width: 80px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />', obj.image.url)
        return format_html('<span style="color: #999;">No image</span>')
    image_preview.short_description = 'Preview'
    
    def image_full_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 100%; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);" />', obj.image.url)
        return format_html('<span style="color: #999;">No image uploaded</span>')
    image_full_preview.short_description = 'Full Preview'
    
    def mark_as_main(self, request, queryset):
        # First, unmark all images for the affected products
        products = set(queryset.values_list('product_id', flat=True))
        for product_id in products:
            ProductImage.objects.filter(product_id=product_id).update(is_main=False)
        
        # Then mark the selected images as main
        queryset.update(is_main=True)
        self.message_user(request, f"{queryset.count()} images marked as main")
    mark_as_main.short_description = 'Set as main product image'
    
    def mark_as_not_main(self, request, queryset):
        queryset.update(is_main=False)
        self.message_user(request, f"{queryset.count()} images unmarked as main")
    mark_as_not_main.short_description = 'Unset as main product image'

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'product', 'product_image', 'created_at', 'actions_display']
    list_filter = ['created_at', 'user__is_active']
    search_fields = ['user__username', 'user__email', 'product__name', 'session_id']
    date_hierarchy = 'created_at'
    readonly_fields = ['user_info', 'product_preview']
    list_per_page = 20
    actions = ['convert_to_order']
    
    fieldsets = (
        ('Wishlist Information', {
            'fields': ('user', 'session_id', 'product', 'product_preview'),
        }),
        ('User Information', {
            'fields': ('user_info',),
            'classes': ('collapse',),
        }),
    )
    
    def user_display(self, obj):
        if obj.user:
            return format_html('<span style="color: #007bff;">{}</span>', obj.user.username)
        return format_html('<span style="color: #6c757d;">Anonymous ({})...</span>', obj.session_id[:8])
    user_display.short_description = 'User'
    
    def product_image(self, obj):
        image = obj.product.images.filter(is_main=True).first() or obj.product.images.first()
        if image and image.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 50px; border-radius: 4px;" />', image.image.url)
        return ""
    product_image.short_description = 'Image'
    
    def product_preview(self, obj):
        image = obj.product.images.filter(is_main=True).first() or obj.product.images.first()
        html = '<div style="display: flex; align-items: center; gap: 15px;">'
        if image and image.image:
            html += format_html('<img src="{}" style="max-height: 100px; max-width: 100px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />', image.image.url)
        html += format_html('<div><h3 style="margin: 0;">{}</h3><p>${:.2f}</p></div>', obj.product.name, obj.product.price)
        html += '</div>'
        return format_html(html)
    product_preview.short_description = 'Product Preview'
    
    def user_info(self, obj):
        if not obj.user:
            return format_html('<p>Anonymous user (Session ID: {})</p>', obj.session_id)
        
        html = '<div style="padding: 10px; background-color: #f9f9f9; border-radius: 4px;">'
        html += format_html('<p><strong>Username:</strong> {}</p>', obj.user.username)
        html += format_html('<p><strong>Email:</strong> {}</p>', obj.user.email)
        html += format_html('<p><strong>Date joined:</strong> {}</p>', obj.user.date_joined.strftime('%Y-%m-%d'))
        html += '</div>'
        return format_html(html)
    user_info.short_description = 'User Information'
    
    def actions_display(self, obj):
        return format_html('<a class="button" href="{}?product_id={}&wishlist_id={}" target="_blank">Add to Cart</a>', 
                          '/cart/add/', obj.product.id, obj.id)
    actions_display.short_description = 'Actions'
    
    def convert_to_order(self, request, queryset):
        # This would typically create an order from wishlist items
        # For now, just show a message
        self.message_user(request, f"{queryset.count()} wishlist items would be converted to orders")
    convert_to_order.short_description = 'Convert to Order'
