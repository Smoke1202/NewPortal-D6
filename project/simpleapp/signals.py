from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import Post, User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime


@receiver(post_save, sender=Post)
def notify_users_news(sender, instance, created, **kwargs):
    if created:
        list_of_subscribers = []
        for c in instance.category.all():
            for usr in c.subscribers.all():
                list_of_subscribers.append(usr.pk)

        for usr_pk in list_of_subscribers:
            email_notifying.apply_async([instance.id, created, usr_pk], countdown=5)


@receiver
def email_notifying(pk, created, usr_pk):

    full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])
    instance = Post.objects.get(pk=pk)
    if created:
        usr = User.objects.get(pk=usr_pk)
        html_content = render_to_string(
            'subs_email.html',
            {
                'post': instance,
                'usr': usr,
                'full_url': full_url,
                'created': created,
            }
        )

        msg = EmailMultiAlternatives(
            subject=instance.title,
            body=f'Здравствуй, {usr.first_name} {usr.last_name}. Новая статья в твоём любимом разделе!'+instance.text,  #  это то же, что и message
            from_email='Christopherga@yandex.ru',
            to=[f'{usr.email}'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем
    else:
        usr = User.objects.get(pk=usr_pk)

        html_content = render_to_string(
            'subs_email.html',
            {
                'post': instance,
                'usr': usr,
                'full_url': full_url,
                'created': created,
            }
        )

        msg = EmailMultiAlternatives(
            subject=instance.title,
            body=f'Здравствуй, {usr.first_name} {usr.last_name}. Cтатья в твоём любимом разделе отредактирована!'+instance.text,  #  это то же, что и message
            from_email='Christopherga@yandex.ru',
            to=[f'{usr.email}'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем


@receiver
def week_email_sending():
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=7)
    full_url = ''.join(['http://', get_current_site(None).domain, ':8000'])

    for u in User.objects.all():
        if len(u.category_set.all()) > 0:
            list_of_posts = Post.objects.filter(date_posted__range=(start_date, end_date), category__in=u.category_set.all())
            if len(list_of_posts) > 0:
                html_content = render_to_string(
                    'subs_email_each_month.html',
                    {
                        'news': list_of_posts,
                        'usr': u,
                        'full_url': full_url,
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=list_of_posts.title,
                    body=f'Здравствуй, {u.first_name} {u.last_name}. Мы подготовили дайджест статей за неделю с нашего портала!',
                    # это то же, что и message
                    from_email='Christopherga@yandex.ru',
                    to=[f'{u.email}'],  # это то же, что и recipients_list
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html

                msg.send()  # отсылаем
