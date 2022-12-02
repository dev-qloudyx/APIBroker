# Create your tasks here
from celery import shared_task
from apps.apibroker.case import CaseSystem

@shared_task
def save_to_db(**kwargs):
    return CaseSystem.create_case(**kwargs)

@shared_task
def update_to_db(**kwargs):
    return CaseSystem.update_case(**kwargs)
