
import base64
import json
import xmltodict
import logging
from apps.apibroker.models import Case, UserCase
from apps.users.models import User
from apps.apibroker.file_validator import data_type
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString  # pretty xml

logger = logging.getLogger(__name__)


class CaseHelper():
    """
    CRUD operations goes here...
    """

    # Data Retrieve
    def get_case_list(*args, **kwargs):
        if kwargs['user'].role == 1:
            try:
                case = Case.objects.all()
                return case
            except:
                case = None
                return case
        else:
            try:
                user = UserCase.objects.get(owner_id=kwargs['user'].id)
                case = Case.objects.filter(customer_key=user.customer_key)
                return case
            except:
                case = None
                return case

    # Data Retrieve
    def get_case_by_filter(*args, **kwargs):
        try:
            user = UserCase.objects.get(owner_id=kwargs['owner'].id)
            kwargs.pop('owner')
            kwargs['customer_key'] = user.customer_key
            case = Case.objects.filter(**kwargs).order_by('-created')
            return case
        except:
            case = None
            return case

    # Data Retrieve
    def get_case_pk(*args, **kwargs):
        try:
            user = UserCase.objects.get(owner_id=kwargs['owner'].id)
            case = Case.objects.filter(
                id=kwargs['id'], customer_key=user.customer_key)
            return case
        except:
            case = None
            return case

class CaseCore():
    """
    Core Methods goes here...
    """

    # Data Conversion
    def to_xml(*args, **kwargs):
        """
        Convert dict to xml
        """
        try:
            #xml_pretty = parseString(xml_bytes).toprettyxml()
            #xml_pretty_decoded = str(xml_pretty).encode('utf-8')
            xml_decoded = str(bytes(dicttoxml(
                kwargs['dict'], root=False, attr_type=False)).decode('utf-8')).encode('utf-8')
            base64_xml_with_doc_filter = base64.b64encode(
                xml_decoded).decode("utf-8")
            return base64_xml_with_doc_filter
        except:
            logger.error('Conversion Dict to Xml Failed...')
            return False

    # Data Conversion
    def to_json(*args, **kwargs):
        """
        Convert dict to json
        """
        try:
            #json_attachments = json.dumps(kwargs['dict'], indent = 4,  ensure_ascii=False).encode('utf8')
            json_attachments = json.dumps(
                kwargs['dict'], ensure_ascii=False).encode('utf8')
            decoded = json_attachments.decode("utf-8")
            json_with_doc_filter_encode = str(decoded).encode("utf-8")
            base64_json_with_doc_filter = base64.b64encode(
                json_with_doc_filter_encode).decode("utf-8")
            return base64_json_with_doc_filter
        except:
            logger.error('Conversion Dict to Json Failed...')
            return False

    # Data Validation
    def isbase64(binary):
        """
        Check if original file is b64 encoded
        """
        try:
            decoded = base64.b64decode(binary)  # Data Validation
            encoded = base64.b64encode(decoded).decode(
                "utf-8")  # Data Validation
            return encoded == binary
        except Exception as e:
            logger.error(str(e))
            return False

    # Data Retrieve
    def search(doc_type, dict, key):
        """
        Filter the Attachment Node by doc_type value
        """
        return [element for element in dict if element[key].lower() == doc_type.lower()]

    # Data Conversion
    def convert_file_into_dict(file_type, xml_mime, file_enconding, json_mime, **kwargs):
        if file_type in xml_mime:
            try:
                dict = xmltodict.parse(
                    kwargs['binary'], encoding=file_enconding)  # Data Conversion
                return dict, True
            except Exception as e:
                logger.error('Conversion XML to DICT Failed')
                return False, str(e)
        elif file_type in json_mime:
            try:
                data_json = bytes(kwargs['binary']).decode(
                    file_enconding)  # Data Conversion
                dict = json.loads(data_json)  # Data Conversion
                return dict, True
            except Exception as e:
                logger.error('Conversion JSON to DICT Failed')
                return False, str(e)
        else:
            return False, f"Allowed types {xml_mime} and {json_mime}"

    # Data Generation
    def case_without_attachment(request, output, dict):
        if request.method == "GET":
            try: 
                del dict['Case']['Message']['Attachments']
                if output is not None and 'xml' == output.lower():
                    base64_xml = CaseSystem.to_xml(
                        dict=dict)  # Data Conversion
                    return base64_xml, None
                elif output is None or output.lower() == 'json':
                    base64_json = CaseSystem.to_json(dict=dict)
                    return base64_json, None
                else:
                    return False, "output must be json or xml"
            except: 
                return False, None
        else:
            return False, "Use GET method..."
        
    # Data Generation
    def case_with_all_attachment(request, output, dict):
        if request.method == "POST": 
            if output is not None and 'xml' == output.lower():
                base64_xml = CaseSystem.to_xml(
                    dict=dict)  # Data Conversion
                return base64_xml, None
            elif output is not None and 'json' == output.lower():
                base64_json = CaseSystem.to_json(
                    dict=dict)  # Data Conversion
                return base64_json, None
            else:
                return False, "output value must be (xml or json)"
        else:
            return False, "Use POST method..."

    # Data Generation
    def case_with_attachment_filter(request, doc_type, dict, output):
        if request.method == "POST":
            if doc_type and not doc_type.lower() == "all":
                if (dict['Case']['Message']['Attachments']['Attachment']):
                    list_of_attachments = CaseSystem.search(
                        doc_type, dict['Case']['Message']['Attachments']['Attachment'], "doc_type")
                else:
                    return False, "No attachments available"
                try: 
                    del dict['Case']['Message']
                    if list_of_attachments:
                        dict['Case']['Message'] = {'Attachments': {'Attachment': list_of_attachments}}
                        if output is not None and 'xml' == output.lower():
                            base64_xml = CaseSystem.to_xml(
                                dict=dict)  # Data Conversion
                            return base64_xml, None
                        elif output is None or 'json' == output.lower():
                            base64_json = CaseSystem.to_json(
                                dict=dict)  # Data Conversion
                            return base64_json, None
                        else:
                            return False, "output must be json or xml"
                    else:
                        return False, "No results"
                except: 
                    return False, None
            elif doc_type and doc_type.lower() == "all":
                dict['Case']['Message'] = {'Attachments': {'Attachment': dict['Case']['Message']['Attachments']['Attachment']}}
                if output is not None and output.lower() == 'xml':
                    base64_xml = CaseSystem.to_xml(
                        dict=dict)  # Data Conversion
                    return base64_xml, None
                elif output is None or output.lower() == 'json':
                    base64_json = CaseSystem.to_json(dict=dict)
                    return base64_json, None
                else:
                    return False, "output must be json or xml"
            else:
                return False, "Use GET for all attachments..."
        if request.method == "GET":
            dict['Case']['Message'] = {'Attachments': {'Attachment': dict['Case']['Message']['Attachments']['Attachment']}}
            if output is not None and output.lower() == 'xml':
                base64_xml = CaseSystem.to_xml(
                    dict=dict)  # Data Conversion
                return base64_xml, None
            elif output is None or output.lower() == 'json':
                base64_json = CaseSystem.to_json(dict=dict)
                return base64_json, None
            else:
                return False, "output must be json or xml"
        else:
            return False, "Use POST or GET method..."
        

class CaseSystem(CaseCore):

    # Data Generation Core
    def generate_case(*args, **kwargs):
        """
        Generate an file without any attachments
        Generate an file case by requested attachment doc_type
        Generate an file with all attachments
        """
        xml_mime = ['application/xml', 'text/xml']
        json_mime = ['application/json']
        # Return mimetype and file encoding
        file_type, file_enconding = data_type(kwargs['binary'])
        doc_type, output, request = kwargs['doc_type'], kwargs['output'], kwargs['request']
    
        # Convert Xml or Json to python dict with the right codec from original file
        dict, msg = CaseSystem.convert_file_into_dict(file_type, xml_mime, file_enconding, json_mime, **kwargs)

        # Attachment filter
        if(dict):
            if kwargs['attachment'] is None:
                result, msg = CaseSystem.case_with_all_attachment(request, output, dict)
                return result, msg
            elif kwargs['attachment']:
                result, msg = CaseSystem.case_with_attachment_filter(request, doc_type, dict, output)
                return result, msg
            elif not kwargs['attachment']:
                result, msg = CaseSystem.case_without_attachment(request, output, dict)
                return result, msg
        else:
            return False, msg
            
    # Data Creation
    def create_case(**kwargs):
        """
        Insert a new case into database by task
        """
        user = User.objects.get(id=kwargs['owner'])
        binary = bytes(base64.b64decode(kwargs['case_file']))
        try:
            case = Case.objects.create(client_key=kwargs['client_key'], customer_key=kwargs['customer_key'], case_number=kwargs['case_number'],
                                       plate_number=kwargs['plate_number'], preshared_key=kwargs['preshared_key'], owner=user, binary=binary)
            logger.info(f'Caso com id: {case.id} criado com sucesso...')
        except Exception as e:
            logger.error(str(e))
