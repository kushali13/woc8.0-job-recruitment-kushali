from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin with user_type in list_display"""
    
    list_display = ['username', 'email', 'user_type', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['user_type', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('User Type', {'fields': ('user_type',)}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('User Type', {'fields': ('user_type',)}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User Profile Admin with customized display"""
    
    list_display = ['user', 'user_type_display', 'phone_number', 'company_name', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email', 'company_name', 'skills']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Common Information', {
            'fields': ('address', 'phone_number')
        }),
        ('Job Seeker Information', {
            'fields': ('resume', 'skills', 'portfolio_url'),
            'classes': ('collapse',)
        }),
        ('Employer Information', {
            'fields': ('company_name', 'website', 'industry', 'description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_type_display(self, obj):
        """Display user type in list view"""
        return obj.user.get_user_type_display()
    user_type_display.short_description = 'User Type'
