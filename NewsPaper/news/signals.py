from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from .models import Post

@receiver(post_save, sender=Post)
def email_new_post_on_category(sender, instance, **kwargs):
    postCategory_list = instance.postCategory.all()
    for category in postCategory_list:
        for sub in category.subscribes.all():
            html_content = render_to_string('email/new_post.html',
                                            {
                                                'user': sub,
                                                'post': instance,
                                            })

            msg = EmailMultiAlternatives(
                subject=f'{instance.title}',
                body="",
                from_email='testpochta@ya.ru',
                to=[f'{sub.email}']

            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()