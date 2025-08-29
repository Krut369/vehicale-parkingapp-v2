# celery_worker.py
from app import create_app
from app.tasks.celery_config import celery

flask_app = create_app()

celery.conf.update(flask_app.config)

# Optional: Tie app context to celery tasks
TaskBase = celery.Task
class ContextTask(TaskBase):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask
