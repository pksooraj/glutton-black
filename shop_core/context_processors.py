from django.contrib.auth.models import User
from shop_products.models import Product, WishlistItem
from shop_orders.models import Order

def admin_stats(request):
    """
    Context processor to provide statistics for the admin dashboard.
    This will only be calculated for admin pages to avoid unnecessary database queries.
    """
    # Only calculate stats for admin pages
    if not request.path.startswith('/admin/'):
        return {}
    
    # Only calculate if user is authenticated and is staff
    if not request.user.is_authenticated or not request.user.is_staff:
        return {}
    
    return {
        'product_count': Product.objects.count(),
        'order_count': Order.objects.count(),
        'wishlist_count': WishlistItem.objects.count(),
        'user_count': User.objects.count(),
    }