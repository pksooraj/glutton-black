from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Testimonial
from django import forms

class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'shop_testimonials/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 10
    
    def get_queryset(self):
        return Testimonial.objects.filter(is_active=True)

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'rating', 'content', 'photo']
        widgets = {
            'rating': forms.RadioSelect(),
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience with our products...'}),
        }

class TestimonialCreateView(CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'shop_testimonials/testimonial_form.html'
    success_url = reverse_lazy('shop_testimonials:testimonial_list')
    
    def form_valid(self, form):
        # If user is authenticated, associate testimonial with user
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        messages.success(self.request, 'Thank you for your testimonial! It will be reviewed shortly.')
        return super().form_valid(form)

def featured_testimonials(request):
    """
    Returns a few featured testimonials for display on the home page
    """
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-rating', '-created_at')[:3]
    return render(request, 'shop_testimonials/featured_testimonials.html', {'testimonials': testimonials})
