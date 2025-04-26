from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import Order, OrderItem
from shop_cart.cart import Cart
import stripe

# Initialize Stripe with the secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Process the checkout form
        form_data = request.POST
        
        if cart.is_empty():
            messages.error(request, 'Your cart is empty')
            return redirect('shop_cart:cart_detail')
            
        # Create a new order
        order = Order(
            first_name=form_data.get('first_name'),
            last_name=form_data.get('last_name'),
            email=form_data.get('email'),
            address=form_data.get('address'),
            city=form_data.get('city'),
            state=form_data.get('state'),
            postal_code=form_data.get('postal_code'),
            country=form_data.get('country'),
            phone=form_data.get('phone')
        )
        
        # Associate with user if logged in
        if request.user.is_authenticated:
            order.user = request.user
        else:
            # Store session ID for anonymous users
            order.session_id = request.session.session_key
            
        order.save()
        
        # Create order items from cart
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'] if 'product' in item else None,
                custom_design=item['custom_design'] if 'custom_design' in item else None,
                price=item['price'],
                quantity=item['quantity'],
                size=item['size']
            )
        
        # Clear the cart
        cart.clear()
        
        # Redirect to payment
        return redirect(reverse('shop_orders:payment', args=[order.id]))
    
    return render(request, 'shop_orders/checkout.html', {
        'cart': cart,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })

def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Create a Stripe checkout session
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(order.total_cost * 100),  # Convert to cents
                        'product_data': {
                            'name': f'Order #{order.id}',
                            'description': f'Black T-Shirts Order',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('shop_orders:payment_success', args=[order.id])),
            cancel_url=request.build_absolute_uri(reverse('shop_orders:payment_cancel', args=[order.id])),
            client_reference_id=str(order.id),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        messages.error(request, f'Error processing payment: {str(e)}')
        return redirect('shop_cart:cart_detail')

def payment_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'processing'
    order.save()
    return render(request, 'shop_orders/payment_success.html', {'order': order})

def payment_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop_orders/payment_cancel.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop_orders/order_history.html', {'orders': orders})

def order_detail(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    else:
        # For anonymous users, check session ID
        session_id = request.session.session_key
        order = get_object_or_404(Order, id=order_id, session_id=session_id)
    
    return render(request, 'shop_orders/order_detail.html', {'order': order})
