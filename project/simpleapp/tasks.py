from celery import shared_task
from .models import Post, Category
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import time

@shared_task
def my_job():
    post_dict = {}
    users_dict = {}
    list_of_posts = []
    list_of_users = []
    tags_subs = {}
    for name in Category.objects.all():
        post_dict[name.name] = Post.objects.filter(date_posted=datetime.fromtimestamp(datetime.timestamp(datetime.now()) - 60), category=name)
        users_dict[name.name] = Category.objects.get(name=name).subscribers.all()
        list_of_posts.append(Post.objects.filter(date_posted=datetime.fromtimestamp(datetime.timestamp(datetime.now()) - 60), category=name))

    for name in Category.objects.all():
        posts = post_dict[name.name]
        users = users_dict[name.name]
        emails = []
        for user in users:
            emails.append(user.email)
        html_content = render_to_string(
            '../templates/weekly_subscription.html',
            {
                'posts': posts, 'name': name.name,
            }
        )
        msg = EmailMultiAlternatives(
            subject='Недельная рассылка новостей',
            body='',
            from_email='Christopherga@yandex.ru',
            to= emails
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()