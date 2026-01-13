from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User Model with user_type field"""
    
    USER_TYPE_CHOICES = [
        ('employer', 'Employer'),
        ('job_seeker', 'Job Seeker'),
    ]
    
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='job_seeker',
        help_text="Select whether you are an Employer or Job Seeker"
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class UserProfile(models.Model):
    """User Profile Model supporting both Employer and Job Seeker roles"""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Job Seeker field
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True, help_text="List your skills (comma-separated or new lines)")
    portfolio_url = models.URLField(blank=True, null=True)
    
    # Employer fields
    company_name = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True, help_text="Company description")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user.user_type == 'employer':
            return f"{self.user.username} - {self.company_name or 'No Company'}"
        else:
            return f"{self.user.username} - Job Seeker Profile"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
