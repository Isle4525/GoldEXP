from django.contrib import admin
from .models import Post, Tag, PostRating

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    # prepopulated_fields = {'slug': ('name',)}  # добавление slug в Tag

class PostRatingInline(admin.TabularInline):
    model = PostRating
    extra = 0
    readonly_fields = ('user', 'value', 'created_at')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'updated_at', 'is_published', 'views')
    list_filter = ('category', 'is_published', 'created_at', 'tags')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}  # добавление slug в Post
    filter_horizontal = ('tags',)
    readonly_fields = ('views', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'category', 'content')
        }),
        ('Медиа', {
            'fields': ('image',)
        }),
        ('Метаданные', {
            'fields': ('tags', 'is_published')
        }),
        ('Статистика', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [PostRatingInline]

admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
