from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem
from shop_products.models import Product
import uuid

def _get_or_create_session_id(request):
    """Helper function to get or create a session ID for anonymous users"""
    if not request.session.get('cart_id'):
        request.session['cart_id'] = str(uuid.uuid4())
    return request.session['cart_id']

def cart_detail(request):
    """View for displaying the shopping cart"""
    # Get cart items based on user or session
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        session_id = _get_or_create_session_id(request)
        cart_items = CartItem.objects.filter(session_id=session_id)
    
    # Calculate totals
    subtotal = sum(item.total_price for item in cart_items)
    tax = subtotal * 0.08  # 8% tax rate
    total = subtotal + tax + 5.00  # $5 shipping
    
    return render(request, 'shop_cart/cart_detail.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    })

def add_to_cart(request, product_id):
    """View for adding a product to the cart"""
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size', 'M')
    quantity = int(request.POST.get('quantity', 1))
    
    # Get or create cart item
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
    else:
        session_id = _get_or_create_session_id(request)
        cart_item, created = CartItem.objects.get_or_create(
            session_id=session_id,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
    
    # If item already exists, update quantity
    if not created:
        cart_item.quantity += quantity
        cart_item.save()
    
    return redirect('shop_cart:cart_detail')

def remove_from_cart(request, item_id):
    """View for removing an item from the cart"""
    if request.method != 'POST':
        return redirect('shop_cart:cart_detail')
        
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Check if user is authorized to remove this item
    if request.user.is_authenticated:
        if cart_item.user != request.user:
            return redirect('shop_cart:cart_detail')
    else:
        session_id = _get_or_create_session_id(request)
        if cart_item.session_id != session_id:
            return redirect('shop_cart:cart_detail')
    
    cart_item.delete()
    return redirect('shop_cart:cart_detail')

def update_cart(request, item_id):
    """View for updating cart item quantity"""
    if request.method != 'POST':
        return redirect('shop_cart:cart_detail')
        
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Check if user is authorized to update this item
    if request.user.is_authenticated:
        if cart_item.user != request.user:
            return redirect('shop_cart:cart_detail')
    else:
        session_id = _get_or_create_session_id(request)
        if cart_item.session_id != session_id:
            return redirect('shop_cart:cart_detail')
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('shop_cart:cart_detail')
