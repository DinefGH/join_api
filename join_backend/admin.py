from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
from .models import CustomUser, Contact, Category, Task, Subtask
from django.utils.translation import gettext_lazy as _



"""
ContactAdmin:

Manages the display, filtering, and searching of Contact records in the admin interface. 
Allows admins to view and manage contacts based on user and other criteria.
"""

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'color', 'user', 'id')  # Columns to display in the admin list view
    list_filter = ('user',)  # Filters by user in the sidebar
    search_fields = ('name', 'email', 'phone')  # Fields to search by in the admin
    ordering = ('user', 'name')  # Default ordering
    raw_id_fields = ('user',)  # Use a lookup widget for user field

admin.site.register(Contact, ContactAdmin)


"""
CustomUserAdmin:

Configures the admin interface for managing CustomUser records, including displaying key user details, 
managing permissions, and controlling the registration and search functionalities.
"""

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



"""
CategoryAdmin:

Handles the display and search capabilities for Category records in the admin interface, 
with filters available for color and name.
"""

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')  # Fields to be displayed in the admin list view
    search_fields = ('name',)  # Fields to search by in the admin
    list_filter = ('color', 'name',)  # Filters by color in the sidebar


admin.site.register(Category, CategoryAdmin)


"""
SubtaskInline:

Defines an inline admin interface for managing Subtasks directly within the Task editing interface, 
facilitating the addition of multiple subtasks.
"""

class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1


"""
TaskAdmin:

Manages the Task records in the admin interface, providing options to filter, 
search, and order tasks by priority, due date, and other key attributes.
"""

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'due_date', 'category', 'creator', 'status')
    list_filter = ('priority', 'due_date', 'category', 'creator', 'status')
    search_fields = ('title', 'description', 'creator__name', 'status')

admin.site.register(Task, TaskAdmin)

"""
SubtaskAdmin:

Configures the display and filtering options for Subtasks in the admin interface, 
allowing for efficient management of subtask completion status and details.
"""

class SubtaskAdmin(admin.ModelAdmin):
    list_display = ['text', 'completed', 'id']  # Adjust fields to display as needed
    list_filter = ['completed']  # Filter options
    search_fields = ['text']  # Search functionality based on text field

admin.site.register(Subtask, SubtaskAdmin)