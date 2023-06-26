from django.contrib import admin

from app_main.models import Category, Language, Code, ImageCode


# Register your models here.

class ImageCodeInline(admin.TabularInline):
    model = ImageCode
    extra = 2


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'category', 'language')
    list_per_page = 10
    list_filter = ('category', 'language')
    inlines = [ImageCodeInline]


admin.site.register(Category)
admin.site.register(Language)
