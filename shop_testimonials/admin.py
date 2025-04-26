from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_active', 'created_at']
    list_filter = ['rating', 'is_active', 'created_at']
    search_fields = ['name', 'content']
    list_editable = ['is_active']
