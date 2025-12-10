from django.contrib import admin
from .models import Emergency, ComunicateEmergencyDepartment


@admin.register(Emergency)
class EmergencyAdmin(admin.ModelAdmin):
    list_display = ('code_emergency', 'type_emergency', 'emergency_status', 'date_time', 'created_by')
    search_fields = ('type_emergency', 'subtype_emergency', 'code_emergency')
    list_filter = ('emergency_status', 'type_emergency', 'date_time')
    ordering = ('-date_time',)
    readonly_fields = ('code_emergency',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('code_emergency', 'type_emergency', 'subtype_emergency', 'emergency_status')
        }),
        ('Location', {
            'fields': ('lat', 'lon', 'date_time')
        }),
        ('Dates', {
            'fields': ('date_open', 'date_standby', 'date_in_progress', 'date_close')
        }),
        ('Relations', {
            'fields': ('emergency_main', 'created_by')
        }),
    )


@admin.register(ComunicateEmergencyDepartment)
class ComunicateEmergencyDepartmentAdmin(admin.ModelAdmin):
    list_display = ('code_emergency', 'code_department')
    search_fields = ('code_emergency__type_emergency', 'code_department__name')
    list_filter = ('code_department',)
