from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from .models import CustomUser, Contact
from django.utils.translation import gettext_lazy as _


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'color', 'user')  # Columns to display in the admin list view
    list_filter = ('user',)  # Filters by user in the sidebar
    search_fields = ('name', 'email', 'phone')  # Fields to search by in the admin
    ordering = ('user', 'name')  # Default ordering
    raw_id_fields = ('user',)  # Use a lookup widget for user field

admin.site.register(Contact, ContactAdmin)

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'is_active', 'is_staff']
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)