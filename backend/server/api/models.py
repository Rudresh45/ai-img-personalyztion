from django.db import models

# Create your models here.

class PersonalizationRequest(models.Model):
    """Model to track photo personalization requests"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    uploaded_photo = models.ImageField(upload_to='uploads/')
    illustration = models.ImageField(upload_to='illustrations/', null=True, blank=True)
    result_image = models.ImageField(upload_to='results/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    error_message = models.TextField(null=True, blank=True)
    face_confidence = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Request {self.id} - {self.status}"
