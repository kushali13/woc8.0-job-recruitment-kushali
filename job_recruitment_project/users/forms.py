from django import forms
from django.core.exceptions import ValidationError
from .models import User, UserProfile


class UserRegistrationForm(forms.ModelForm):
    """User Registration Form with user_type selection"""
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        help_text="Password must be at least 8 characters long."
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'user_type', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")
        
        return password_confirm
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserProfileEditForm(forms.ModelForm):
    """User Profile Edit Form with custom validation"""
    
    class Meta:
        model = UserProfile
        fields = ['address', 'phone_number', 'resume', 'skills', 'portfolio_url', 
                  'company_name', 'website', 'industry', 'description']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'resume': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
    
    def clean_resume(self):
        """Custom validation: Resume must be PDF only"""
        resume = self.cleaned_data.get('resume')
        
        if resume:
            # Check if file exists and has a name
            if hasattr(resume, 'name'):
                # Check file extension
                if not resume.name.lower().endswith('.pdf'):
                    raise ValidationError("Resume must be a PDF file. Please upload a .pdf file.")
                
                # Check file size (max 5MB)
                if resume.size > 5 * 1024 * 1024:
                    raise ValidationError("Resume file size must be less than 5MB.")
        
        return resume

