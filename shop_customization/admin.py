from django.contrib import admin
from .models import CustomDesign

@admin.register(CustomDesign)
class CustomDesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'design_type', 'size', 'quantity', 'price', 'created_at')
    list_filter = ('design_type', 'size', 'created_at')
    search_fields = ('custom_text',)
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
