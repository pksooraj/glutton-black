from django.conf import settings
from .models import CartItem
from shop_products.models import Product

class Cart:
    def __init__(self, request):
        """Initialize the cart"""
        self.request = request
        self.session = request.session
        
        # Get cart items based on user or session
        if request.user.is_authenticated:
            self.cart_items = CartItem.objects.filter(user=request.user)
        else:
            # Get or create session ID
            if not self.session.get('cart_id'):
                self.session['cart_id'] = self._generate_session_id()
            self.cart_items = CartItem.objects.filter(session_id=self.session['cart_id'])
    
    def _generate_session_id(self):
        """Generate a unique session ID for anonymous users"""
        import uuid
        return str(uuid.uuid4())
    
    def add(self, product, quantity=1, size='M', update_quantity=False):
        """Add a product to the cart or update its quantity"""
        product_id = product.id if isinstance(product, Product) else product
        product_obj = Product.objects.get(id=product_id)
        
        # Get or create cart item
        if self.request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=self.request.user,
                product=product_obj,
                size=size,
                defaults={'quantity': quantity}
            )
        else:
            cart_item, created = CartItem.objects.get_or_create(
                session_id=self.session['cart_id'],
                product=product_obj,
                size=size,
                defaults={'quantity': quantity}
            )
        
        # Update quantity if needed
        if not created and update_quantity:
            cart_item.quantity = quantity
        elif not created:
            cart_item.quantity += quantity
        
        cart_item.save()
    
    def remove(self, cart_item_id):
        """Remove a cart item"""
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
    
    def update_quantity(self, cart_item_id, quantity):
        """Update the quantity of a cart item"""
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            pass
    
    def clear(self):
        """Remove all items from cart"""
        if self.request.user.is_authenticated:
            CartItem.objects.filter(user=self.request.user).delete()
        else:
            CartItem.objects.filter(session_id=self.session['cart_id']).delete()
    
    def is_empty(self):
        """Check if cart is empty"""
        return self.cart_items.count() == 0
    
    def __iter__(self):
        """Iterate over the cart items"""
        for item in self.cart_items:
            yield {
                'id': item.id,
                'product': item.product,
                'price': item.product.price,
                'quantity': item.quantity,
                'size': item.size,
                'total_price': item.total_price
            }
    
    def __len__(self):
        """Count all items in the cart"""
        return self.cart_items.count()
    
    @property
    def subtotal(self):
        """Calculate subtotal price"""
        return sum(item.total_price for item in self.cart_items)
    
    @property
    def tax(self):
        """Calculate tax (8%)"""
        return self.subtotal * 0.08
    
    @property
    def shipping(self):
        """Shipping cost"""
        return 5.00 if self.subtotal > 0 else 0.00
    
    @property
    def total(self):
        """Calculate total price"""
        return self.subtotal + self.tax + self.shipping