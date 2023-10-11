from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives


def get_all_subscriptions(category):
    user_email = []
    for user in category.subscribes.all():
        user_email.append(user_email)
    return user_email


def task_post_sub_weekly(instance, category):
    template = 'email/sub_week_post_catgory.html'
    user_emails = get_all_subscriptions(category)
    email_subject = f'Еженедельная рассылка вашей любимой категории - "{category}"'
    html = render_to_string(
        template_name=template,
        context={
            'category': category,
            'posts': instance,
        },
    )
    msg = EmailMultiAlternatives(
        subject=email_subject,
        body='',
        from_email='testpochta@ya.ru',
        to=user_emails
    )
    msg.attach_alternative(html, 'text/html')
    msg.send()
