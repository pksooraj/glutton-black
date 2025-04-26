// Custom animations using GSAP and AOS

document.addEventListener('DOMContentLoaded', function() {
    // Initialize GSAP animations
    
    // Hero section text animation with enhanced effects
    gsap.from('.hero-text', {
        duration: 1.5,
        y: 60,
        opacity: 0,
        stagger: 0.3,
        ease: 'power3.out',
        onComplete: function() {
            // Add a subtle pulse effect after the initial animation
            gsap.to('.hero-text', {
                scale: 1.03,
                duration: 1.2,
                repeat: 1,
                yoyo: true,
                ease: 'power1.inOut'
            });
        }
    });
    
    // Add page transition effect
    gsap.to('body', {
        opacity: 1,
        duration: 0.5,
        ease: 'power2.out'
    });
    
    // Initialize testimonial slider with Slick with enhanced animations
    if($('.testimonial-slider').length) {
        $('.testimonial-slider').slick({
            dots: true,
            arrows: true,
            infinite: true,
            speed: 800,
            slidesToShow: 3,
            slidesToScroll: 1,
            autoplay: true,
            autoplaySpeed: 5000,
            cssEase: 'cubic-bezier(0.645, 0.045, 0.355, 1.000)',
            fade: false,
            centerMode: true,
            centerPadding: '60px',
            responsive: [
                {
                    breakpoint: 1024,
                    settings: {
                        slidesToShow: 2,
                        slidesToScroll: 1,
                        centerMode: true,
                        centerPadding: '40px'
                    }
                },
                {
                    breakpoint: 640,
                    settings: {
                        slidesToShow: 1,
                        slidesToScroll: 1,
                        centerMode: true,
                        centerPadding: '40px'
                    }
                }
            ]
        });
        
        // Add entrance animation for slider
        gsap.from('.testimonial-slider', {
            opacity: 0,
            y: 50,
            duration: 1,
            ease: 'power3.out',
            scrollTrigger: {
                trigger: '.testimonial-slider',
                start: 'top bottom-=100',
                toggleActions: 'play none none none'
            }
        });
    }
    
    // Enhanced parallax effect for hero background
    gsap.to('.parallax-bg', {
        yPercent: 30,
        ease: 'none',
        scrollTrigger: {
            trigger: '.parallax-bg',
            start: 'top top',
            end: 'bottom top',
            scrub: 0.5
        }
    });
    
    // Add depth effect to hero section
    gsap.to('.hero-text', {
        y: 50,
        ease: 'none',
        scrollTrigger: {
            trigger: '.hero-text',
            start: 'top top',
            end: 'bottom top',
            scrub: 0.8
        }
    });
    
    // Enhanced button hover animations
    const buttons = document.querySelectorAll('.animated-btn, button[type="submit"], a.bg-black');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', () => {
            gsap.to(button, {
                scale: 1.05,
                duration: 0.3,
                ease: 'power2.out',
                boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
            });
        });
        
        button.addEventListener('mouseleave', () => {
            gsap.to(button, {
                scale: 1,
                duration: 0.3,
                ease: 'power2.out',
                boxShadow: 'none'
            });
        });
        
        // Add click animation
        button.addEventListener('mousedown', () => {
            gsap.to(button, {
                scale: 0.98,
                duration: 0.1,
                ease: 'power2.out'
            });
        });
        
        button.addEventListener('mouseup', () => {
            gsap.to(button, {
                scale: 1.05,
                duration: 0.2,
                ease: 'power2.out'
            });
        });
    });
    
    // Enhanced product card hover animations
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        // Create a timeline for smoother coordinated animations
        const cardTl = gsap.timeline({ paused: true });
        
        // Add animations to the timeline
        if (card.querySelector('img')) {
            cardTl.to(card.querySelector('img'), {
                scale: 1.1,
                duration: 0.5,
                ease: 'power2.out'
            }, 0);
        }
        
        if (card.querySelector('.card-overlay')) {
            cardTl.to(card.querySelector('.card-overlay'), {
                opacity: 1,
                duration: 0.3
            }, 0);
        }
        
        // Add subtle lift effect
        cardTl.to(card, {
            y: -10,
            boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
            duration: 0.4,
            ease: 'power2.out'
        }, 0);
        
        // Play timeline on hover
        card.addEventListener('mouseenter', () => cardTl.play());
        card.addEventListener('mouseleave', () => cardTl.reverse());
        
        // Add click animation
        card.addEventListener('mousedown', () => {
            gsap.to(card, {
                scale: 0.98,
                duration: 0.1,
                ease: 'power2.in'
            });
        });
        
        card.addEventListener('mouseup', () => {
            gsap.to(card, {
                scale: 1,
                duration: 0.2,
                ease: 'power2.out'
            });
        });
    });
    
    // Newsletter form animation
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        const formElements = newsletterForm.querySelectorAll('input, button');
        formElements.forEach(element => {
            element.addEventListener('focus', () => {
                gsap.to(element, {
                    boxShadow: '0 0 0 3px rgba(255,255,255,0.3)',
                    duration: 0.3
                });
            });
            
            element.addEventListener('blur', () => {
                gsap.to(element, {
                    boxShadow: 'none',
                    duration: 0.3
                });
            });
        });
    }
    
    // Enhanced AOS animations
    // These will add more variety to the existing AOS animations
    const aosElements = document.querySelectorAll('[data-aos]');
    aosElements.forEach((element, index) => {
        // Add random delays to create a more dynamic feel
        const delay = 50 + (index % 5) * 50;
        element.setAttribute('data-aos-delay', delay.toString());
        
        // Add different animation durations
        const duration = 600 + (index % 3) * 100;
        element.setAttribute('data-aos-duration', duration.toString());
    });
    
    // Reinitialize AOS with new settings
    AOS.refresh();
});

// Add scroll-triggered animations with enhanced effects
window.addEventListener('scroll', function() {
    // Parallax effect for hero image
    const heroImage = document.querySelector('.parallax-bg');
    if (heroImage) {
        const scrollPosition = window.pageYOffset;
        heroImage.style.transform = `translateY(${scrollPosition * 0.4}px) scale(${1 + scrollPosition * 0.0002})`;
    }
    
    // Add subtle rotation to some elements on scroll
    const rotateElements = document.querySelectorAll('.product-card img');
    if (rotateElements.length) {
        const scrollPercent = window.pageYOffset / (document.body.offsetHeight - window.innerHeight);
        rotateElements.forEach((el, index) => {
            const rotationAmount = (index % 2 === 0 ? 1 : -1) * scrollPercent * 5;
            el.style.transform = `rotate(${rotationAmount}deg)`;
        });
    }
});

// Enhanced Instagram feed hover effects
document.addEventListener('DOMContentLoaded', function() {
    // Instagram feed hover animations with improved effects
    const instagramItems = document.querySelectorAll('.grid .product-card a');
    
    instagramItems.forEach(item => {
        // Create a timeline for coordinated animations
        const instaTl = gsap.timeline({ paused: true });
        
        if (item.querySelector('img')) {
            instaTl.to(item.querySelector('img'), {
                scale: 1.1,
                duration: 0.5,
                ease: 'power2.out'
            }, 0);
        }
        
        if (item.querySelector('.card-overlay')) {
            instaTl.to(item.querySelector('.card-overlay'), {
                backgroundColor: 'rgba(0,0,0,0.4)',
                opacity: 1,
                duration: 0.3
            }, 0);
        }
        
        if (item.querySelector('svg')) {
            instaTl.to(item.querySelector('svg'), {
                scale: 1.2,
                rotation: 10,
                duration: 0.3,
                ease: 'back.out(1.7)'
            }, 0.1);
        }
        
        // Add subtle border glow
        instaTl.to(item, {
            boxShadow: '0 0 20px rgba(255,255,255,0.3)',
            duration: 0.4
        }, 0);
        
        // Play timeline on hover
        item.addEventListener('mouseenter', () => instaTl.play());
        item.addEventListener('mouseleave', () => instaTl.reverse());
        
        // Add click animation
        item.addEventListener('mousedown', () => {
            gsap.to(item, {
                scale: 0.95,
                duration: 0.1,
                ease: 'power2.in'
            });
        });
        
        item.addEventListener('mouseup', () => {
            gsap.to(item, {
                scale: 1,
                duration: 0.2,
                ease: 'power2.out'
            });
        });
    });
    
    // Add form validation and animations for payment forms
    const paymentForms = document.querySelectorAll('form');
    paymentForms.forEach(form => {
        const inputs = form.querySelectorAll('input');
        
        // Add focus animations to form inputs
        inputs.forEach(input => {
            input.addEventListener('focus', () => {
                gsap.to(input, {
                    borderColor: '#000',
                    boxShadow: '0 0 0 3px rgba(0,0,0,0.1)',
                    duration: 0.3
                });
                
                // Animate the label if it exists
                const label = input.previousElementSibling;
                if (label && label.tagName === 'LABEL') {
                    gsap.to(label, {
                        y: -3,
                        color: '#000',
                        fontWeight: 'bold',
                        duration: 0.3
                    });
                }
            });
            
            input.addEventListener('blur', () => {
                if (!input.value) {
                    gsap.to(input, {
                        borderColor: '#e2e8f0',
                        boxShadow: 'none',
                        duration: 0.3
                    });
                    
                    // Reset the label animation if input is empty
                    const label = input.previousElementSibling;
                    if (label && label.tagName === 'LABEL') {
                        gsap.to(label, {
                            y: 0,
                            color: '#4a5568',
                            fontWeight: 'normal',
                            duration: 0.3
                        });
                    }
                }
            });
            
            // Add validation visual feedback
            input.addEventListener('input', () => {
                if (input.checkValidity()) {
                    gsap.to(input, {
                        borderColor: '#68d391',
                        duration: 0.3
                    });
                } else {
                    gsap.to(input, {
                        borderColor: input.value ? '#fc8181' : '#e2e8f0',
                        duration: 0.3
                    });
                }
            });
        });
        
        // Add form submission animation
        form.addEventListener('submit', function(e) {
            // Only add animation, don't prevent default as it needs to submit
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                gsap.to(submitBtn, {
                    scale: 0.95,
                    duration: 0.1,
                    onComplete: () => {
                        gsap.to(submitBtn, {
                            scale: 1,
                            duration: 0.3
                        });
                    }
                });
            }
        });
    });
    
    // Add page transition effects
    const links = document.querySelectorAll('a:not([target="_blank"])');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            // Don't apply to links with specific classes or attributes
            if (link.classList.contains('no-transition') || link.getAttribute('data-no-transition')) {
                return;
            }
            
            const href = link.getAttribute('href');
            // Only apply to internal links
            if (href && href.indexOf('#') !== 0 && href.indexOf('javascript:') !== 0) {
                e.preventDefault();
                
                // Create page transition effect
                const overlay = document.createElement('div');
                overlay.style.position = 'fixed';
                overlay.style.top = '0';
                overlay.style.left = '0';
                overlay.style.width = '100%';
                overlay.style.height = '100%';
                overlay.style.backgroundColor = '#000';
                overlay.style.zIndex = '9999';
                overlay.style.opacity = '0';
                document.body.appendChild(overlay);
                
                // Animate overlay and then navigate
                gsap.to(overlay, {
                    opacity: 0.5,
                    duration: 0.3,
                    onComplete: () => {
                        window.location.href = href;
                    }
                });
            }
        });
    });
});

// Initialize AOS with enhanced settings
document.addEventListener('DOMContentLoaded', function() {
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: false,
        mirror: true
    });
});
                scale: 1,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });
});