from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin

@admin.register(User)
class UserAdmin(UserBaseAdmin):

        ordering = ("email",)
        # Fields displayed in admin listing
        list_display = (
        "email", "first_name", "last_name", 
        "is_staff", "is_active", "is_superuser", "blocked", "strikes"
        )
        search_fields = ("email", "first_name", "last_name")
        list_filter = ("is_staff", "is_active", "is_superuser", "blocked", "sex", "blood_type")

        fieldsets = (
                ("👤 Account Information", {
                "fields": ("email", "password", "first_name", "last_name")
                }),
                ("⚙️ Permissions and Access", {
                    "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
                }),
                ("📍 Personal Data", {
                    "fields": ("identificator", "address", "phone_number", "sex", "age", "height", "weight", "blood_type")
                }),
                ("💊 Medical Information", {
                    "fields": (
                        "allergies", "allergies_other",
                        "chronic_diseases", "chronic_diseases_other",
                        "previous_surgeries", "previous_surgeries_other",
                        "disabilities", "disabilities_other"
                    )
                }),
                ("📞 Emergency Contacts", {
                    "fields": ("close_contacts",)
                }),
                ("🔐 OAuth", {
                    "fields": ("google_id", "is_oauth_user")
                }),
                ("⚠️ Warning System", {
                    "fields": ("strikes", "blocked")
                }),
                ("🕒 Audit", {
                    "fields": ("last_login", "date_joined", "updated_at")
                }),
        )
        readonly_fields = ("updated_at", "last_login", "date_joined")
        add_fieldsets = (
            (None, {
                "classes": ("wide",),
                "fields": ("email","identificator","password1", "password2"),
            }),
        )
@admin.register(Allergy)
class AllergyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")  # columns in listing
    search_fields = ("name",)                          # search by name
    list_filter = ("is_active",)                       # filter by status
    ordering = ("name",)                               # alphabetical order
    readonly_fields = ("created_at",)                  # not editable


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