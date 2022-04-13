from django.shortcuts import render
from .forms import PostForm
from django.core.paginator import Paginator
from .models import Post, Category
from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .filters import PostFilter
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-date_posted')
    paginate_by = 5

    def get_context(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['value1'] = None
        return context

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs


def search(request):
    f = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'search.html', {'filter': f})


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()


class NewsCreateView(CreateView):
    template_name = 'news_create.html'
    form_class = PostForm
    success_url = '/news/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class NewsUpdateView(UpdateView):
    template_name = 'news_create.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    context_object_name = 'new'
    success_url = '/news/'


@login_required
def subscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    if category not in user.category_set.all():
        category.subscribers.add(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_me(request, pk):
    user = request.user
    print('Пользователь', request.user, 'отписался от новостей категории:', Category.objects.get(pk=pk))
    category = Category.objects.get(id=pk)
    if category in user.category_set.all():
        category.subscribers.remove(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))