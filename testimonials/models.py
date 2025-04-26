from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='testimonials/%Y/%m/%d', blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Testimonial by {self.name}'