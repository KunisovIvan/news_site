from django import template
from news.models import Category
from django.db.models import Count, F

register = template.Library()

#Определение функции-тега, необходимой для исключения дублирования кода,
# при получении из модели Category всех данных о категориях
@register.simple_tag()
def get_categories():
    return Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)

# @register.simple_tag()
# def show_categories():
#     return Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt_gt=0)