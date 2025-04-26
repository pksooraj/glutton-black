from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
import uuid
from .models import Product, WishlistItem

def _get_or_create_session_id(request):
    """Helper function to get or create a session ID for anonymous users"""
    if not request.session.get('wishlist_id'):
        request.session['wishlist_id'] = str(uuid.uuid4())
    return request.session['wishlist_id']

def product_list(request):
    """
    View for displaying all products
    """
    # In a real implementation, this would fetch from the database
    # For now, we'll use dummy data if no products exist in the database
    products = Product.objects.all()
    
    # If no products in database, create sample products
    if not products.exists():
        sample_products = [
            {'name': 'Classic Black Tee', 'price': 29.99, 'description': 'Premium quality black t-shirt made from 100% organic cotton.', 'short_description': 'Our signature classic black tee'},
            {'name': 'Minimalist Logo Tee', 'price': 34.99, 'description': 'Clean, minimalist design on our premium black t-shirt.', 'short_description': 'Simple, elegant, minimalist'},
            {'name': 'Urban Black Tee', 'price': 32.99, 'description': 'Street-inspired design for the urban lifestyle.', 'short_description': 'Perfect for city life'},
            {'name': 'Vintage Black Tee', 'price': 36.99, 'description': 'Distressed look with a vintage feel.', 'short_description': 'Classic vintage style'},
            {'name': 'Athletic Black Tee', 'price': 39.99, 'description': 'Performance fabric for active lifestyles.', 'short_description': 'Built for movement'},
            {'name': 'Graphic Print Tee', 'price': 33.99, 'description': 'Bold graphic design on premium cotton.', 'short_description': 'Make a statement'},
        ]
        
        for product_data in sample_products:
            Product.objects.create(**product_data)
        
        products = Product.objects.all()
    
    # Get user's wishlist items
    wishlist_items = []
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        session_id = _get_or_create_session_id(request)
        wishlist_items = WishlistItem.objects.filter(session_id=session_id).values_list('product_id', flat=True)
    
    return render(request, 'shop_products/product_list.html', {
        'products': products,
        'wishlist_items': wishlist_items
    })

def product_detail(request, product_id):
    """
    View for displaying a single product's details
    """
    # Get the product from the database
    product = get_object_or_404(Product, id=product_id)
    
    # Check if product is in user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()
    else:
        session_id = _get_or_create_session_id(request)
        in_wishlist = WishlistItem.objects.filter(session_id=session_id, product=product).exists()
    
    # Get related products
    related_products = Product.objects.exclude(id=product_id)[:4]
    
    return render(request, 'shop_products/product_detail.html', {
        'product': product,
        'in_wishlist': in_wishlist,
        'related_products': related_products
    })

@require_POST
def add_to_wishlist(request, product_id):
    """
    Add a product to the user's wishlist
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Check if already in wishlist
    if request.user.is_authenticated:
        wishlist_item, created = WishlistItem.objects.get_or_create(
            user=request.user,
            product=product
        )
    else:
        session_id = _get_or_create_session_id(request)
        wishlist_item, created = WishlistItem.objects.get_or_create(
            session_id=session_id,
            product=product
        )
    
    if created:
        messages.success(request, f"{product.name} has been added to your wishlist!")
    else:
        messages.info(request, f"{product.name} is already in your wishlist.")
    
    # Redirect back to the referring page
    next_url = request.POST.get('next', 'shop_products:product_list')
    return redirect(next_url)

@require_POST
def remove_from_wishlist(request, product_id):
    """
    Remove a product from the user's wishlist
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Remove from wishlist
    if request.user.is_authenticated:
        WishlistItem.objects.filter(user=request.user, product=product).delete()
    else:
        session_id = _get_or_create_session_id(request)
        WishlistItem.objects.filter(session_id=session_id, product=product).delete()
    
    messages.success(request, f"{product.name} has been removed from your wishlist.")
    
    # Redirect back to the referring page
    next_url = request.POST.get('next', 'shop_products:product_list')
    return redirect(next_url)

def wishlist(request):
    """
    View for displaying the user's wishlist
    """
    # Get wishlist items
    if request.user.is_authenticated:
        wishlist_items = WishlistItem.objects.filter(user=request.user).select_related('product')
    else:
        session_id = _get_or_create_session_id(request)
        wishlist_items = WishlistItem.objects.filter(session_id=session_id).select_related('product')
    
    return render(request, 'shop_products/wishlist.html', {
        'wishlist_items': wishlist_items
    })
