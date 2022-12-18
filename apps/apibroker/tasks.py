# Create your tasks here
from celery import shared_task
from apps.apibroker.case import CaseSystem

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries':10, 'countdown': 5})
def save_to_db(**kwargs):
    case = CaseSystem.create_case(**kwargs)
    return f"CaseID: {case.id}, Owner: {case.owner}, OperatorID: {case.operatorId}"

