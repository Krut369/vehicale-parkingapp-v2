# celery_beat.py
from app import create_app
from app.tasks.celery_config import celery
from celery.schedules import crontab
from app.tasks.daily_reminder import send_daily_reminders, send_weekly_summary

flask_app = create_app()

celery.conf.update(flask_app.config)

# Configure Celery Beat Schedule
celery.conf.beat_schedule = {
    'daily-reminders': {
        'task': 'app.tasks.daily_reminder.send_daily_reminders',
        'schedule': crontab(hour=9, minute=0),  # Every day at 9:00 AM
    },
    'weekly-summaries': {
        'task': 'app.tasks.daily_reminder.send_weekly_summary',
        'schedule': crontab(day_of_week=0, hour=10, minute=0),  # Every Sunday at 10:00 AM
    },
}

# Optional: Tie app context to celery tasks
TaskBase = celery.Task
class ContextTask(TaskBase):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask

if __name__ == '__main__':
    celery.start() 