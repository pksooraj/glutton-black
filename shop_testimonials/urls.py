from django.urls import path
from . import views

app_name = 'shop_testimonials'

urlpatterns = [
    path('testimonials/', views.TestimonialListView.as_view(), name='testimonial_list'),
    path('testimonials/add/', views.TestimonialCreateView.as_view(), name='testimonial_add'),
    path('featured-testimonials/', views.featured_testimonials, name='featured_testimonials'),
]