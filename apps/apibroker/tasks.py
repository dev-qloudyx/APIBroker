# Create your tasks here
from celery import shared_task
from apps.apibroker.cases import CaseSystem

@shared_task
def save_to_db(**kwargs):
    return CaseSystem.create_case(**kwargs)


# @shared_task(bind=True)
# def execute(self, *args, **kwargs):
#     UploadVideo.execute_scheduled_upload(self, *args, **kwargs)
