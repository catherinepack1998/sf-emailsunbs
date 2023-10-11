# from django.shortcuts import render
from audioop import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView, DeleteView
from .models import Category, Post
from datetime import datetime
from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PostsList(ListView):
    model = Post
    template_name = 'news/posts.html'
    form_class = PostForm
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-createData')
    paginate_by = 10

    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['time_now'] = timezone.localtime(timezone.now())
       context['value1'] = None
       context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
       context['form'] = PostForm()
       context['username'] = self.request.user.username
       context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
       return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            form.save()
        return super().get(request, *args, **kwargs)

class PostDetailView(DetailView):
   template_name = 'news/post_detail.html'
   queryset = Post.objects.all()
   
   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['username'] = self.request.user.username
    context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
    return context

# дженерик для создания объекта. Надо указать только имя шаблона и класс формы, который мы написали в прошлом юните. Остальное он сделает за вас
class PostCreateView(PermissionRequiredMixin, CreateView):
   permission_required = ('news.add_post')
   template_name = 'news/post_create.html'
   form_class = PostForm

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['username'] = self.request.user.username
    context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
    return context

class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.user.username
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context

class PostCategoryView(LoginRequiredMixin, DetailView):
    model = Category
    template_name = 'news/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(id=self.kwargs['pk'])
        context['subscribers'] = category.subscribes.all()
        context['username'] = self.request.user.username
        context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
        return context

# дженерик для редактирования объекта
class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
   permission_required = ('news.change_post')
   template_name = 'news/post_create.html'
   form_class = PostForm

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['username'] = self.request.user.username
    context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
    return context

   def get_object(self, **kwargs):
       id = self.kwargs.get('pk')
       return Post.objects.get(pk=id)

class PostDeleteView(PermissionRequiredMixin, DeleteView):
   permission_required = ('news.delete_post')
   template_name = 'news/post_delete.html'
   queryset = Post.objects.all()
   success_url = reverse_lazy('news:posts')
   
   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['username'] = self.request.user.username
    context['is_author'] = self.request.user.groups.filter(name = 'authors').exists()
    return context

class PostSearch(LoginRequiredMixin, PostsList):
    template_name = 'news/post_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
def subscribe_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribes.add(request.user.id)
    return HttpResponseRedirect('../../category/{0}'.format(pk))


def unsubscribe_category(request, pk):
    category = Category.objects.get(pk=pk)
    category.subscribes.remove(request.user.id)
    return HttpResponseRedirect('../../category/{0}'.format(pk))