# app/tasks/celery_config.py
from celery import Celery

def make_celery(app_name='vehicle_parking_app'):
    return Celery(
        app_name,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0'
    )

celery = make_celery()
