from django.urls import path
from .views import PostList, PostDetail, NewsDetailView, NewsDeleteView, NewsCreateView, NewsUpdateView, search,\
    subscribe_me, unsubscribe_me

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search', search),
    path('<int:pk>/', NewsDetailView.as_view()),
    path('create/', NewsCreateView.as_view()),
    path('delete/<int:pk>', NewsDeleteView.as_view()),
    path('update/<int:pk>', NewsUpdateView.as_view()),
    path('subscribe/<int:pk>', subscribe_me),
    path('unsubscribe/<int:pk>', unsubscribe_me),
]