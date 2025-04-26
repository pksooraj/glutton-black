from django.shortcuts import render, redirect
from django.contrib import messages
from shop_testimonials.models import Testimonial
from shop_products.models import Product


def home(request):
    """
    View for the home page that displays featured products and testimonials
    """
    # Get featured products from the database
    featured_products = Product.objects.filter(is_featured=True)[:3]
    
    # Get testimonials from the database
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-rating', '-created_at')[:3]
    
    return render(request, 'core/home.html', {
        'featured_products': featured_products,
        'testimonials': testimonials
    })

def about(request):
    """
    View for the about page
    """
    return render(request, 'core/about.html')

def contact(request):
    """
    View for the contact page
    """
    if request.method == 'POST':
        # Process contact form
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # In a real implementation, you would send an email or save to database
        # For now, just show a success message
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('core:contact')
        
    return render(request, 'core/contact.html')


def newsletter_signup(request):
    """
    Handle newsletter signup form submission
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        # In a real implementation, you would save this to the database
        messages.success(request, f'Thank you for subscribing with {email}!')
    return redirect('core:home')
