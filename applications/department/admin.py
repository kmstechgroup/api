from django.contrib import admin
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'email')
    list_filter = ()
    ordering = ('name',)
    readonly_fields = ('jurisdiction_expanded',)  # Read-only because it is calculated automatically
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'address', 'phone', 'email')
        }),
        ('Jurisdiction', {
            'fields': ('jurisdiction', 'jurisdiction_expanded'),
            'description': 'jurisdiction_expanded is automatically calculated as a 1km buffer around jurisdiction'
        }),
    )
