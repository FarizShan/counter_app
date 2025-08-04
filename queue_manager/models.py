from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('staff', 'Staff Member'),
        ('supervisor', 'Supervisor'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
    

class QueueEntry(models.Model):
    SERVICE_CHOICES = [
        ('General Service', 'General Service'),
        ('Document Processing', 'Document Processing'),
        ('Payment', 'Payment'),
        ('Consultation', 'Consultation'),
        ('Technical Support', 'Technical Support'),
    ]

    customer_name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    token_number = models.CharField(max_length=20, unique=True)
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('waiting', 'Waiting'),
            ('in-progress', 'In Progress'),
            ('completed', 'Completed'),
        ],
        default='waiting'
    )
    
    timestamp = models.DateTimeField(default=timezone.now)  # when added to queue
    started_at = models.DateTimeField(null=True, blank=True)  # when service starts
    completed_at = models.DateTimeField(null=True, blank=True)  # when service completes
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.token_number} - {self.customer_name}"
