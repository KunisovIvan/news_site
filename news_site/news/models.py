from django.db import models
from django.urls import reverse
from crum import get_current_user

from django.contrib.auth.models import User

#Описание модели списка новостей для SQLite3
class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
#Столбец, связанный с моделью Category
    category = models.ForeignKey('Category', related_name='news', on_delete=models.PROTECT, null=True, verbose_name='Категория')
    user = models.ForeignKey('auth.User', related_name='user', on_delete=models.PROTECT, blank=True, null=True, default=None,verbose_name='Пользователь')

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user = user
        super(News, self).save(*args, **kwargs)

#Определение функции для построение ссылки URL на определенную новость
    def get_absolute_url(self):
        return reverse('view_news', kwargs={"news_id": self.pk})

# Определение функции для возвращения нормального названия(title) для новостей в админке и др. местах
    def __str__(self):
        return self.title

# Настройка админки (Названия в ед. и мн. числе, сортировка)
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

#Описание модели списка категорий для SQLite3
class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

# Определение функции для построение ссылки URL на определенную категорию
    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

# Определение функции для возвращения нормального названия(title) для категории в админке и др. местах
    def __str__(self):
        return self.title

# Настройка админки (Названия в ед. и мн. числе, сортировка)
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']

class Comment(models.Model):
     news = models.ForeignKey(News, on_delete=models.PROTECT, related_name='comments', verbose_name='Новость')
     user = models.ForeignKey('auth.User', on_delete=models.PROTECT, blank=True, null=True, default=None,verbose_name='Пользователь')
     context = models.TextField(blank=True, verbose_name='Текст комментария')
     created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
     updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
     is_published = models.BooleanField(default=True, verbose_name='Опубликовать')

     def save(self, *args, **kwargs):
         user = get_current_user()
         if user and not user.pk:
             user = None
         if not self.pk:
             self.user = user
         super(Comment, self).save(*args, **kwargs)

     class Meta:
         verbose_name = 'Коментарий'
         verbose_name_plural = 'Коментарии'
         ordering = ('-created_at',)

     def __str__(self):
         return 'Комментарий с автором "{}" к новости "{}"'.format(self.user, self.news)





