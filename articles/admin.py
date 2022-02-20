from django.contrib import admin

from .models import Article, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'date', 'author',)
    prepopulated_fields = {'slug': ('title', )}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body', 'article', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Article, ArticleAdmin)
