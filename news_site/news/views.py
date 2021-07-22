from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.core.mail import send_mail

from .forms import NewsForm, CommentForm, ContactForm
from .models import News, Category, Comment


def contact(request):
      if request.method == 'POST':
          form = ContactForm(data=request.POST)
          if form.is_valid():
              mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'site_test_django@mail.ru',
                               ['kunisov.ivan@mail.ru'], fail_silently=True)
              if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
              else:
                messages.error(request, 'Ошибка отправки')
          else:
            messages.error(request, 'Ошибка отправки')
      else:
          form = ContactForm()
      return render(request, 'news/contact.html', {'form': form, 'title': 'Обратная связь'})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserCreationForm()
    return render(request, 'news/register.html', {'form': form, 'title': 'Регистрация'})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'news/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

#Класс-контроллер для главной страницы
class HomeNews(ListView):
    model = News
    template_name = 'news/index.html' #news_list
    context_object_name = 'news' #object_list
    # extra_context = {'title': 'Главная'} #Передача статичных данных
    paginate_by = 5

    #Функция для передачи данных в шаблон
    def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Главная страница'
            return context

    #Добавляем Where к SQL-запросу, для выводв только опубликованнх новостей
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category', 'user')

# # Функция контроллер(вьюха), для рендера данными и возвращения нужного шаблона,
# # в ответ на запрос пользователя по связанному URL
# # Возвращает шаблон с главной страницей
# def index(request):
#     news = News.objects.all()
#      context = {
#          'news': news,
#         'title': 'Список новостей',
#      }
#      return render(request, 'news/index.html', context)

#Класс-контроллер для страницы с нужной категорией
class NewsByCategory(ListView):
    model = News
    template_name = 'news/index.html'  # news_list
    context_object_name = 'news'  # object_list
    # allow_empty = False #Для вывода ошибки 404 при пустом list
    paginate_by = 5

    # extra_context = {'title': 'Категория'}

    # Функция для передачи данных в шаблон
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return context

    # Добавляем Where к SQL-запросу, для выводв только опубликованнх новостей
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category', 'user')

# #Функция контроллер(вьюха), для рендера данными и возвращения нужного шаблона,
# # в ответ на запрос пользователя по связанному URL
# #Возвращает шаблон с новостями из нужной категгории
# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = get_object_or_404(Category, pk=category_id)
#     return render(request, ''news/index.html'', {'news': news, 'category':category})

#Класс-контроллер для страницы с конктретной новостью
# class ViewNews(DetailView):
#     model = News
#     context_object_name = 'news'
#     # pk_url_kwarg = 'news_id' #Для построение ссылки в url.py при news/<int:news_id>/ и kwargs={"news_id": self.pk},
#                                # а не news/<int:pk>/ и kwargs={"pk": self.pk}
#     template_name = 'news/view_news.html' #news_detail.html
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = get_object_or_404(News, pk=self.kwargs['pk'])
#         return context


 #Функция контроллер(вьюха), для рендера данными и возвращения нужного шаблона,
 # в ответ на запрос пользователя по связанному URL
 #Возвращает шаблон с одной новостью
def view_news(request, news_id):
    news = get_object_or_404(News, pk=news_id)

    # List of active comments for this post
    comments = news.comments.filter(is_published=True).select_related('user')

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.news = news
            # Save the comment to the database
            new_comment.save()
            messages.success(request, 'Комментарий добавлен')
            return redirect(news)
    else:
        comment_form = CommentForm()
    return render(request,
                  'news/view_news.html',
                  {'news': news,
                   'comments': comments,
                   'comment_form': comment_form,
                   'news_id': news_id,
                   'title': news.title})

#Класс-контроллер для страницы с формой
class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home') #Если необходимо редиректить на другую страницу,
                                         # необходимо подключить библиотеку reverse_lazy

    def get_context_data(self, *, object_list=None, **kwargs):
            context = super().get_context_data(**kwargs)
            context['title'] = 'Добавить новость'
            return context



# #Функция контроллер(вьюха), для рендера данными и возвращения нужного шаблона,
# # в ответ на запрос пользователя по связанному URL.
# #Получение данных из форм, проверка на валидность, push в модель
# #Возвращает шаблон с формой, для добавления новости
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})
