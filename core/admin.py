from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings, Program, NewsCategory, News, Staff,
    Application, ContactMessage, GalleryImage, Document, FAQ,
)

admin.site.site_header = "2-son texnikumi - Boshqaruv paneli"
admin.site.site_title = "Texnikum admin"
admin.site.index_title = "Sayt boshqaruvi"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Asosiy", {"fields": ("name", "short_name", "slogan", "about_short", "founded_year", "logo")}),
        ("Aloqa", {"fields": ("address", "phone", "email", "work_hours", "ministry", "map_embed")}),
        ("Ijtimoiy tarmoqlar", {"fields": ("telegram", "instagram", "facebook", "youtube")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "duration", "grant_places", "contract_places", "order", "is_active")
    list_editable = ("order", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "description")


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_at", "is_published", "views")
    list_filter = ("is_published", "category")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "role", "order")
    list_filter = ("role",)
    list_editable = ("order",)
    search_fields = ("full_name", "position")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "program", "phone", "status", "created_at")
    list_filter = ("status", "program")
    list_editable = ("status",)
    search_fields = ("full_name", "phone", "email")
    readonly_fields = ("created_at",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "phone", "is_read", "created_at")
    list_filter = ("is_read",)
    list_editable = ("is_read",)
    readonly_fields = ("created_at",)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "uploaded_at")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)
