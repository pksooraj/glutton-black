document.addEventListener('DOMContentLoaded', function() {
    // Get all cart items
    const cartItems = document.querySelectorAll('.product-card');
    
    // Initialize cart functionality for each item
    cartItems.forEach(item => {
        const decreaseBtn = item.querySelector('button:first-of-type');
        const increaseBtn = item.querySelector('button:last-of-type');
        const quantityInput = item.querySelector('input[type="number"]');
        const priceElement = item.querySelector('.text-xl.font-medium');
        const removeBtn = item.querySelector('.remove-btn');
        const itemId = item.dataset.itemId;
        
        // Store original price per item
        const originalPrice = parseFloat(priceElement.textContent.replace('$', '')) / parseInt(quantityInput.value);
        
        // Add hover effect to cart item
        item.addEventListener('mouseenter', function() {
            this.classList.add('shadow-md');
            this.style.transform = 'translateY(-2px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.classList.remove('shadow-md');
            this.style.transform = 'translateY(0)';
        });
        
        // Get the form element
        const form = item.querySelector('form');
        
        // Decrease quantity button
        decreaseBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
                updatePrice();
                // Submit the form after a short delay
                setTimeout(() => {
                    form.submit();
                }, 300);
            }
        });
        
        // Increase quantity button
        increaseBtn.addEventListener('click', function() {
            let currentValue = parseInt(quantityInput.value);
            quantityInput.value = currentValue + 1;
            updatePrice();
            // Submit the form after a short delay
            setTimeout(() => {
                form.submit();
            }, 300);
        });
        
        // Update price when quantity changes
        quantityInput.addEventListener('change', function() {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue < 1) {
                currentValue = 1;
                quantityInput.value = 1;
            }
            updatePrice();
            // Submit the form
            form.submit();
        });
        
        // Remove item button
        removeBtn.addEventListener('click', function() {
            item.style.opacity = '0';
            item.style.height = '0';
            item.style.overflow = 'hidden';
            item.style.padding = '0';
            item.style.margin = '0';
            item.style.border = 'none';
            
            // Remove item after animation completes
            setTimeout(() => {
                // Find the remove form and submit it
                const removeForm = item.querySelector('form[action*="remove"]');
                if (removeForm) {
                    removeForm.submit();
                }
            }, 500);
        });
        });
        
        // Update price based on quantity
        function updatePrice() {
            const quantity = parseInt(quantityInput.value);
            const newPrice = (originalPrice * quantity).toFixed(2);
            priceElement.textContent = `$${newPrice}`;
            
            // Update order summary
            updateOrderSummary();
        }
        
        // No need for updateCart function as we're using form submissions now
    });
    
    // Checkout button animation
    const checkoutBtn = document.querySelector('.checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('mouseenter', function() {
            this.classList.add('scale-105');
            this.style.boxShadow = '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)';
        });
        
        checkoutBtn.addEventListener('mouseleave', function() {
            this.classList.remove('scale-105');
            this.style.boxShadow = 'none';
        });
    }
    
    // Update order summary totals - only for visual feedback before form submission
    function updateOrderSummary() {
        const prices = Array.from(document.querySelectorAll('.product-card .text-xl.font-medium'))
            .map(el => parseFloat(el.textContent.replace('$', '')));
        
        const subtotal = prices.reduce((sum, price) => sum + price, 0);
        const tax = subtotal * 0.08; // Assuming 8% tax rate
        const total = subtotal + tax + 5.00; // Adding $5 shipping
        
        // Make sure these elements exist before trying to update them
        const subtotalElement = document.querySelector('.order-summary .border-b .flex:first-child span:last-child');
        const taxElement = document.querySelector('.order-summary .border-b .flex:last-child span:last-child');
        const totalElement = document.querySelector('.order-summary .flex.justify-between.mb-6 span:last-child');
        
        if (subtotalElement) subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
        if (taxElement) taxElement.textContent = `$${tax.toFixed(2)}`;
        if (totalElement) totalElement.textContent = `$${total.toFixed(2)}`;
    }
    
    // Update cart count in header
    function updateCartCount() {
        const cartCount = document.querySelectorAll('.product-card').length;
        const cartCountElement = document.querySelector('.cart-count');
        if (cartCountElement) {
            cartCountElement.textContent = cartCount;
            if (cartCount === 0) {
                cartCountElement.classList.add('hidden');
            }
        }
        
        // Update cart header
        const cartHeader = document.querySelector('.border-b.border-gray-200.pb-4.mb-4 h2');
        if (cartHeader) {
            cartHeader.textContent = `Shopping Cart (${cartCount} items)`;
        }
    }
    
    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});