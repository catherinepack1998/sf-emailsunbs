import logging
from datetime import timedelta, date

from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Post
from news.tasks import task_post_sub_weekly

logger = logging.getLogger(__name__)


def job_weekly():
    d = date.today() - timedelta(days=7)
    weekly_news = Post.objects.filter(dateCreate__gte=d)
    set_category = set()
    for category in weekly_news:
        set_category.add(category)

    task_post_sub_weekly(weekly_news, set_category)

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Запуски планировщика."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")


        scheduler.add_job(
            job_weekly,
            trigger=CronTrigger(day_of_week="mon"),
            id="job_weekly",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена работа таска job_weekly.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),

            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Добавлена еженедельная задача: 'delete_old_job_executions'."
        )

        try:
            logger.info("Запуск планировщика...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика...")
            scheduler.shutdown()
            logger.info("Планировщик успешно завершил работу")