from django.contrib import admin
from .models import Conversation, Message

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'content', 'timestamp', 'is_read')

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'participants_list')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('participants__username',)
    filter_horizontal = ('participants',)
    inlines = [MessageInline]
    
    def participants_list(self, obj):
        return ", ".join([p.username for p in obj.participants.all()])
    participants_list.short_description = "Участники"

class MessageAdmin(admin.ModelAdmin):
    list_display = ('content', 'sender', 'conversation', 'timestamp', 'is_read')
    list_filter = ('timestamp', 'is_read')
    search_fields = ('content', 'sender__username')
    readonly_fields = ('timestamp',)

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)