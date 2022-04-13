from django.template.backends import django
from django_filters import FilterSet, DateFilter
import django.forms
from .models import Post
from django.forms import DateInput
import django_filters


class PostFilter(FilterSet):
    author = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains', label='Автор')
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Заголовок')
    date = django_filters.DateFilter(field_name='date_posted', widget=DateInput(attrs={'type': 'date'}),
                                     lookup_expr='gt', label='Новее этой даты')