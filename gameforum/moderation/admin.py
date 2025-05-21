from django.contrib import admin
from .models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'reporter', 'content_object', 'created_at', 'is_resolved')
    list_filter = ('report_type', 'is_resolved', 'created_at')
    search_fields = ('description', 'reporter__username')
    readonly_fields = ('reporter', 'post', 'comment', 'created_at')
    fieldsets = (
        (None, {
            'fields': ('reporter', 'report_type', 'description')
        }),
        ('Контент', {
            'fields': ('post', 'comment'),
            'classes': ('collapse',)
        }),
        ('Статус', {
            'fields': ('is_resolved',)
        }),
        ('Дата', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def content_object(self, obj):
        return obj.post or obj.comment
    content_object.short_description = "Объект жалобы"

admin.site.register(Report, ReportAdmin)