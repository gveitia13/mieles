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
    exclude = ('user',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superstar: return True
        return obj and obj.user == request.user

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superstar: return True
        return obj and obj.user == request.user


admin.site.register(Category, )
admin.site.register(Language)
