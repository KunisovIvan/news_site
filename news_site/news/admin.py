from django.contrib import admin

from .models import News, Category, Comment
from .forms import NewsAdminForm


#Настройка админки (что показывать, что делать ссылками, по каким полям вести поиск и т.д.)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title', 'category', 'created_at', 'updated_at', 'is_published', 'user')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')

#Настройка админки (что показывать, что делать ссылками, по каким полям вести поиск и т.д.)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'news', 'created_at', 'is_published')
    list_filter = ('id', 'is_published', 'created_at', 'updated_at')
    search_fields = ('user', 'context')



admin.site.register(Comment, CommentAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)
