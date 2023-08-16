from django.contrib import admin
from django.contrib.auth.models import User, Group

from lawyer.models import ContactNumber, ContactInformation, Application

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(ContactNumber)
class ContactNumberAdmin(admin.ModelAdmin):
    list_display = ["number", "whatsapp"]


@admin.register(ContactInformation)
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ["language", "email", "address"]
    readonly_fields = ["language"]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created_at",
        "name",
        "phone_number",
        "email",
    ]
    readonly_fields = [
        "created_at",
    ]
    ordering = [
        "created_at",
    ]
