
import os
from apps.apibroker.models import Case, FileAttachment
from apps.users.models import User
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import uuid


class CaseSystem():

    fs = FileSystemStorage()
    CASE_PATH = os.path.join(fs.path('cases'), '')

    def generate_kwargs(*args,**kwargs):
        kwargs['owner'] = args[0]
        kwargs['customer_key'] = args[1]['customer_key']
        kwargs['case_number'] = args[1]['case_number']
        kwargs['plate_number'] = args[1]['plate_number']
        kwargs['case_files'] = args[2]
        kwargs['update'] = args[3]
        return kwargs

    def filename_generator(file):
        date = datetime.now().strftime("%Y%m%d%H%M%S%f")
        code_rand = uuid.uuid4().hex
        filename = "%s%s_%s" % (code_rand, date, file)
        name = CaseSystem.fs.save(os.path.join(CaseSystem.CASE_PATH,
                                                filename), file) 
        return name

    def save_files(**kwargs):
        case_list_attachment = []
        case_file = kwargs['case_files']
        files = case_file.getlist('case_file')
        files_attachment = case_file.getlist('attachment')
        
        if(kwargs['update']): # Check if it's an update
            if(files):
                case = Case.objects.get(id=kwargs['pk'])
                CaseSystem.fs.delete(str(case.case_file)) # Remove Case File from system storage
            if(files_attachment):
                case_attachment = FileAttachment.objects.filter(case_id=kwargs['pk'])
                if(case_attachment):
                    for i in case_attachment:
                        CaseSystem.fs.delete(str(i.file_attachment)) # Remove Attachment's Files from system storage
        
        case_filename = CaseSystem.filename_generator(files[0]) # Proceed to generate new filename for the case file     
        for f in files_attachment:
            name = CaseSystem.filename_generator(f) # Proceed to generate new filenames for attachment's
            case_list_attachment.append(name)
        return [case_filename, case_list_attachment]

    def create_case(**kwargs):
        case_file = kwargs['filename'][0]
        files_attachments = kwargs['filename'][1]
        user = User.objects.get(id=kwargs['owner'])
        case = Case.objects.create(customer_key=kwargs['customer_key'], case_number=kwargs['case_number'],
                            plate_number=kwargs['plate_number'], owner=user, case_file=case_file)
        
        for f in files_attachments:
            attachment = FileAttachment(file_attachment=f, case_id=case.id)
            attachment.save()
        
    def update_case(**kwargs):
        user = User.objects.get(id=kwargs['owner'])
        case_file = kwargs['filename'][0]
        files_attachments = kwargs['filename'][1]
        Case.objects.filter(id=kwargs['pk']).update(customer_key=kwargs['customer_key'], case_number=kwargs['case_number'],
                            plate_number=kwargs['plate_number'], owner=user, case_file=case_file)
        
        file_attachment = FileAttachment.objects.filter(case_id=kwargs['pk'])
        if(file_attachment):
            for f, b in zip(files_attachments, file_attachment):
                try:
                    case_attch = FileAttachment.objects.get(file_attachment=b.file_attachment)
                    FileAttachment.objects.filter(id=case_attch.id).update(file_attachment=f)
                except FileAttachment.DoesNotExist:
                    obj = FileAttachment(case_id=kwargs['pk'], file_attachment=f)
                    obj.save()
        else:
            for f in files_attachments:
                obj = FileAttachment(case_id=kwargs['pk'], file_attachment=f)
                obj.save()
            

            
    
        
        
        