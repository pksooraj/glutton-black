from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomDesign
from django.views.decorators.http import require_POST
import uuid

def customize(request):
    """
    Display the t-shirt customization interface.
    """
    return render(request, 'shop_customization/customize.html')

@require_POST
def add_custom_to_cart(request):
    """
    Process the customization form and add the custom design to cart.
    """
    design_type = request.POST.get('design_type')
    size = request.POST.get('size', 'M')
    quantity = int(request.POST.get('quantity', 1))
    
    # Create a new custom design
    custom_design = CustomDesign(
        design_type=design_type,
        size=size,
        quantity=quantity
    )
    
    # Set user or session ID
    if request.user.is_authenticated:
        custom_design.user = request.user
    else:
        # Get or create session ID
        if not request.session.session_key:
            request.session.create()
        custom_design.session_id = request.session.session_key
    
    # Handle text design
    if design_type == 'text':
        custom_text = request.POST.get('custom_text', '')
        font_style = request.POST.get('font_style', 'sans-serif')
        custom_design.custom_text = custom_text
        custom_design.font_style = font_style
    
    # Handle image design
    elif design_type == 'upload' and 'image_upload' in request.FILES:
        custom_design.custom_image = request.FILES['image_upload']
        custom_design.design_type = 'image'  # Ensure correct type is set
    
    custom_design.save()
    
    messages.success(request, 'Your custom design has been added to cart!')
    return redirect('cart:cart_detail')
