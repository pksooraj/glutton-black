document.addEventListener('DOMContentLoaded', function() {
    // Size selection functionality
    const sizeOptions = document.querySelectorAll('.size-option input');
    const productForm = document.getElementById('product-form');
    
    // Initialize with default selected size
    let selectedSize = document.querySelector('.size-option input:checked');
    if (selectedSize) {
        selectedSize.parentElement.querySelector('span').classList.add('bg-black', 'text-white');
    }
    
    sizeOptions.forEach(option => {
        option.addEventListener('change', function() {
            // Remove active class from all options
            sizeOptions.forEach(opt => {
                opt.parentElement.querySelector('span').classList.remove('bg-black', 'text-white');
            });
            
            // Add active class to selected option
            this.parentElement.querySelector('span').classList.add('bg-black', 'text-white');
        });
    });
    
    // Quantity buttons functionality
    const quantityInput = document.querySelector('input[name="quantity"]');
    const quantityBtns = document.querySelectorAll('.quantity-btn');
    
    if (quantityInput && quantityBtns.length) {
        // Ensure initial value is valid
        if (parseInt(quantityInput.value) < 1) {
            quantityInput.value = 1;
        }
        
        // Add event listener for manual input changes
        quantityInput.addEventListener('change', function() {
            let value = parseInt(this.value);
            if (isNaN(value) || value < 1) {
                this.value = 1;
            }
        });
        
        quantityBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const action = this.dataset.action;
                let currentValue = parseInt(quantityInput.value);
                
                if (action === 'increase') {
                    quantityInput.value = currentValue + 1;
                } else if (action === 'decrease' && currentValue > 1) {
                    quantityInput.value = currentValue - 1;
                }
            });
        });
    }
    
    // Form submission validation
    if (productForm) {
        productForm.addEventListener('submit', function(e) {
            // Ensure a size is selected
            if (!document.querySelector('.size-option input:checked')) {
                e.preventDefault();
                alert('Please select a size');
                return false;
            }
            
            // Ensure quantity is valid
            const qty = parseInt(quantityInput.value);
            if (isNaN(qty) || qty < 1) {
                e.preventDefault();
                alert('Please enter a valid quantity');
                return false;
            }
        });
    }
});