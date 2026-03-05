from django.contrib import admin
from .models import Document

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'file_name', 'created_at', 'has_content')
    list_filter = ('created_at',)
    search_fields = ('title', 'content', 'file_name')

    # ← Add this line (important!)
    readonly_fields = ('created_at', 'updated_at', 'file_name', 'mime_type', 'content_preview')

    fieldsets = (
        (None, {
            'fields': ('title', 'file')
        }),
        ('Extracted Content', {
            'fields': ('content_preview',),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('file_name', 'mime_type', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    def has_content(self, obj):
        return bool(obj.content.strip())
    has_content.boolean = True
    has_content.short_description = "Has content"

    def content_preview(self, obj):
        if obj.content:
            preview = obj.content[:300] + "..." if len(obj.content) > 300 else obj.content
            return preview.replace('\n', '<br>')
        return "No content extracted yet"
    content_preview.short_description = "Content preview"
    content_preview.allow_tags = True  # deprecated in newer Django → use mark_safe instead if warning appears