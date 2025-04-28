document.addEventListener('DOMContentLoaded', function() {
    // Size selection functionality
    const sizeOptions = document.querySelectorAll('.size-option input');
    const productForm = document.getElementById('product-form');
    
    // Initialize with default selected size
    let selectedSize = document.querySelector('.size-option input:checked');
    if (selectedSize) {
        selectedSize.parentElement.querySelector('span').classList.add('bg-black', 'text-white');
    }
    
    // Ensure product main image is loaded properly
    const mainImage = document.querySelector('.product-main-image');
    if (mainImage) {
        // Make sure image is visible with proper styling
        mainImage.style.display = 'block';
        mainImage.style.margin = '0 auto';
        mainImage.style.maxWidth = '100%';
        mainImage.style.height = 'auto';
        mainImage.style.objectFit = 'contain';
        mainImage.style.minHeight = '300px';
        mainImage.style.opacity = '1';
        
        // Hide loading spinner if it exists
        const loadingSpinner = document.querySelector('.loading-spinner');
        if (loadingSpinner) {
            loadingSpinner.style.display = 'none';
        }
        
        // Add responsive styling for different screen sizes
        const applyResponsiveStyles = () => {
            if (window.innerWidth <= 640) { // Mobile
                mainImage.style.maxHeight = '350px';
                mainImage.style.minHeight = '250px';
            } else if (window.innerWidth <= 768) { // Tablet
                mainImage.style.maxHeight = '400px';
                mainImage.style.minHeight = '300px';
            } else { // Desktop
                mainImage.style.maxHeight = '500px';
                mainImage.style.minHeight = '300px';
            }
        };
        
        // Apply responsive styles initially and on window resize
        applyResponsiveStyles();
        window.addEventListener('resize', applyResponsiveStyles);
        
        // Add error handling for image loading
        mainImage.onerror = function() {
            console.error('Failed to load image:', this.src);
            // Try loading again or use a fallback image
            this.src = '/static/images/product-1.jpg';
        };
    }
    
    // Initialize gallery functionality
    const galleryImages = document.querySelectorAll('.gallery-image');
    if (galleryImages.length > 0) {
        galleryImages.forEach(img => {
            // Ensure thumbnails load properly
            img.onerror = function() {
                this.src = '/static/images/product-1.jpg';
            };
            
            // Make gallery images responsive
            img.style.maxWidth = '100%';
            img.style.height = 'auto';
            img.style.opacity = '1';
            
            // Hide thumbnail spinner if it exists
            const thumbnailSpinner = img.parentElement.querySelector('.thumbnail-spinner');
            if (thumbnailSpinner) {
                thumbnailSpinner.style.display = 'none';
            }
            
            // Add click event to update main image
            img.addEventListener('click', function() {
                // Update main image src with clicked thumbnail src
                if (mainImage) {
                    mainImage.src = this.src;
                    mainImage.style.opacity = '1';
                    
                    // Ensure main image is visible with proper styling
                    mainImage.style.display = 'block';
                    mainImage.style.margin = '0 auto';
                    mainImage.style.maxWidth = '100%';
                    mainImage.style.height = 'auto';
                    mainImage.style.objectFit = 'contain';
                    
                    // Hide loading spinner if it exists
                    const loadingSpinner = document.querySelector('.loading-spinner');
                    if (loadingSpinner) {
                        loadingSpinner.style.display = 'none';
                    }
                }
                
                // Remove active class from all thumbnails
                galleryImages.forEach(thumb => {
                    const container = thumb.parentElement;
                    if (container) {
                        container.classList.remove('ring-2', 'ring-black');
                    }
                });
                
                // Add active class to clicked thumbnail
                const container = this.parentElement;
                if (container) {
                    container.classList.add('ring-2', 'ring-black');
                }
                
                // Scroll to top of image container on mobile
                if (window.innerWidth < 768) {
                    const imageContainer = document.querySelector('.product-image-container');
                    if (imageContainer) {
                        imageContainer.scrollIntoView({behavior: 'smooth', block: 'nearest'});
                    }
                }
            });
        });
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