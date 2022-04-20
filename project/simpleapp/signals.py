from django.db.models.signals import post_save, pre_save, m2m_changed, post_init
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Author, Post, Category, PostCategory
from django.template.loader import render_to_string


@receiver(post_save, sender=Post)
def notify_users_news(sender, instance, created, **kwargs):
    if created:
        list_of_subscribers = []
        for c in instance.category.all():
            for usr in c.subscribers.all():
                list_of_subscribers.append(usr.pk)

        for usr_pk in list_of_subscribers:
            notify_managers_appointment.apply_async([instance.id, created, usr_pk], countdown=5)


@receiver(m2m_changed, sender=PostCategory)
def notify_managers_appointment(sender, instance, **kwargs):
    new_post_category = Post.objects.order_by('-id')[0].category.all()

    list_of_users = []
    for name in new_post_category:
        for i in range(len(Category.objects.get(name=name).subscribers.all())):
            list_of_users.append(Category.objects.get(name=name).subscribers.all()[i].email)
    link_id = instance.id
    link = f'http://127.0.0.1:8000/news/{link_id}'
    html_content = render_to_string(
        '../templates/appointment.html',
        {
            'appointment': instance, 'link': link
        }
    )
    msg = EmailMultiAlternatives(
        subject=f'{instance.title}',
        body=f'{instance.text}',
        from_email='Christopherga@yandex.ru',
        to= list_of_users
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
