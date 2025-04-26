# ... existing code ...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Tailwind
    'tailwind',
    'theme',
    
    # Custom apps
    'core',
    'products',
    'customization',
    'cart',
    'orders',
    'testimonials',
]

TAILWIND_APP_NAME = 'theme'

# ... existing code ...

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')