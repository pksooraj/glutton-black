from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"

class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='collections/')
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-featured', '-created']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('shop_products:collection_detail', args=[self.slug])
