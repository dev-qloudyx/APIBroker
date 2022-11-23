
import os
from apps.apibroker.models import Case
from apps.users.models import User
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import uuid


class CaseSystem():

    fs = FileSystemStorage()
    CASE_PATH = os.path.join(fs.path('cases'), '')

    def save_case_disk(**kwargs):
        case_file = kwargs['case_file']
        date = datetime.now().strftime("%Y%m%d%H%M%S%f")
        code_rand = uuid.uuid4().hex
        filename = "%s%s_%s" % (code_rand, date,case_file)
        name = CaseSystem.fs.save(os.path.join(CaseSystem.CASE_PATH,
                                               filename), case_file)
        return name

    def create_case(**kwargs):
        user = User.objects.get(id=kwargs['owner'])
        Case.objects.create(customer_key=kwargs['customer_key'], case_number=kwargs['case_number'],
                            plate_number=kwargs['plate_number'], case_file=kwargs['filename'], owner=user)
