from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin

@admin.register(User)
class UserAdmin(UserBaseAdmin):
        # Campos que se muestran en el listado del admin
        list_display = (
        "username", "email", "first_name", "last_name", 
        "is_staff", "is_active", "is_superuser", "blocked", "strikes"
        )
        search_fields = ("username", "email", "first_name", "last_name")
        list_filter = ("is_staff", "is_active", "is_superuser", "blocked", "sex", "blood_type")

        fieldsets = (
                ("👤 Información de cuenta", {
                "fields": ("username", "password", "email", "first_name", "last_name")
                }),
                ("⚙️ Permisos y acceso", {
                    "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
                }),
                ("📍 Datos personales", {
                    "fields": ("identificator", "address", "phone_number", "sex", "age", "height", "weight", "blood_type")
                }),
                ("💊 Información médica", {
                    "fields": (
                        "allergies", "allergies_other",
                        "chronic_diseases", "chronic_diseases_other",
                        "previous_surgeries", "previous_surgeries_other",
                        "disabilities", "disabilities_other"
                    )
                }),
                ("📞 Contactos de emergencia", {
                    "fields": ("close_contacts",)
                }),
                ("🔐 OAuth", {
                    "fields": ("google_id", "is_oauth_user")
                }),
                ("⚠️ Sistema de advertencias", {
                    "fields": ("strikes", "blocked")
                }),
                ("🕒 Auditoría", {
                    "fields": ("last_login", "date_joined", "updated_at")
                }),
        )
        readonly_fields = ("updated_at", "last_login", "date_joined")
        add_fieldsets = (
            (None, {
                "classes": ("wide",),
                "fields": ("username", "email","identificator","password1", "password2"),
            }),
        )
@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")  # columnas en el listado
    search_fields = ("name",)                          # buscador por nombre
    list_filter = ("is_active",)                       # filtro por estado
    ordering = ("name",)                               # orden alfabético
    readonly_fields = ("created_at",)                  # no editable


@admin.register(ChronicDisease)
class ChronicDiseaseAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)
    readonly_fields = ("created_at",)


@admin.register(PreviousSurgery)
class PreviousSurgeryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)
    readonly_fields = ("created_at",)


@admin.register(Disability)
class DisabilityAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)
    readonly_fields = ("created_at",)