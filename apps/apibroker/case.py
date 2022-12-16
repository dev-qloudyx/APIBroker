
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

    # Data Creation
    def create_case(**kwargs):
        """
        Insert a new case into database by task
        """
        try:
            user = User.objects.get(id=kwargs['owner'])
            binary = bytes(base64.b64decode(kwargs['case_file']))
            case = Case.objects.create(client_key=kwargs['client_key'], customer_key=kwargs['customer_key'], case_number=kwargs['case_number'],
                                     plate_number=kwargs['plate_number'], preshared_key=kwargs['preshared_key'], owner=user, binary=binary)
            logger.info(f'Caso com id: {case.id} criado com sucesso...')
        except Exception as e:
            logger.error(str(e))

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


class CaseCore(CaseHelper):
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
            # xml_pretty_decoded = str(xml_pretty).encode(kwargs['kwargs['file_enconding']'])
            xml_convert = dicttoxml(kwargs['dict'], root=False, attr_type=False)
            xml_decoded = str(xml_convert.decode("utf-8")).encode(kwargs['file_enconding'])
            base64_xml_with_doc_filter = base64.b64encode(xml_decoded).decode(kwargs['file_enconding'])
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
                kwargs['dict'], ensure_ascii=False).encode(kwargs['file_enconding'])
            decoded = json_attachments.decode(kwargs['file_enconding'])
            json_with_doc_filter_encode = str(
                decoded).encode(kwargs['file_enconding'])
            base64_json_with_doc_filter = base64.b64encode(
                json_with_doc_filter_encode).decode(kwargs['file_enconding'])
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
            file_type, file_enconding = data_type(decoded)  # Data Validation
            encoded = base64.b64encode(decoded).decode(
                file_enconding)  # Data Validation
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
    def convert_file_into_dict(**kwargs):
        if kwargs['file_type'] in kwargs['xml_mime']:
            try:
                dict = xmltodict.parse(
                    kwargs['binary'], encoding=kwargs['file_enconding'])  # Data Conversion
                return dict, True
            except Exception as e:
                logger.error('Conversion XML to DICT Failed')
                return False, str(e)
        elif kwargs['file_type'] in kwargs['json_mime']:
            try:
                data_json = bytes(kwargs['binary']).decode(
                    kwargs['file_enconding'])  # Data Conversion
                dict = json.loads(data_json)  # Data Conversion
                return dict, True
            except Exception as e:
                logger.error('Conversion JSON to DICT Failed')
                return False, str(e)
        else:
            return False, f"Allowed types {kwargs['xml_mime']} and {kwargs['json_mime']}"

    # Data Generation
    def case_without_attachment(**kwargs):
        if kwargs['request'].method == "GET":
            try:
                del kwargs['dict']['Case']['Message']['Attachments']
                if kwargs['output'] is not None and 'xml' == kwargs['output'].lower():
                    base64_xml = CaseSystem.to_xml(**kwargs)  # Data Conversion
                    return base64_xml, None
                elif kwargs['output'] is None or kwargs['output'].lower() == 'json':
                    base64_json = CaseSystem.to_json(**kwargs)
                    return base64_json, None
                else:
                    return False, "kwargs['output'] must be json or xml"
            except:
                return False, None
        else:
            return False, "Use GET method..."

    # Data Generation
    def case_with_all_attachment(**kwargs):
        if kwargs['request'].method == "POST":
            if kwargs['output'] is not None and 'xml' == kwargs['output'].lower():
                base64_xml = CaseSystem.to_xml(**kwargs)  # Data Conversion
                return base64_xml, None
            elif kwargs['output'] is not None and 'json' == kwargs['output'].lower():
                base64_json = CaseSystem.to_json(**kwargs)  # Data Conversion
                return base64_json, None
            else:
                return False, "kwargs['output'] value must be (xml or json)"
        else:
            return False, "Use POST method..."

    # Data Generation
    def case_with_attachment_filter(**kwargs):
        if kwargs['request'].method == "POST":
            if kwargs['doc_type'] and not kwargs['doc_type'].lower() == "all":
                if (kwargs['dict']['Case']['Message']['Attachments']['Attachment']):
                    list_of_attachments = CaseSystem.search(
                        kwargs['doc_type'], kwargs['dict']['Case']['Message']['Attachments']['Attachment'], "doc_type")
                else:
                    return False, "No attachments available"
                try:
                    del kwargs['dict']['Case']['Message']
                    if list_of_attachments:
                        kwargs['dict']['Case']['Message'] = {'Attachments': {
                            'Attachment': list_of_attachments}}
                        if kwargs['output'] is not None and 'xml' == kwargs['output'].lower():
                            base64_xml = CaseSystem.to_xml(**kwargs)  # Data Conversion
                            return base64_xml, None
                        elif kwargs['output'] is None or 'json' == kwargs['output'].lower():
                            base64_json = CaseSystem.to_json(**kwargs)  # Data Conversion
                            return base64_json, None
                        else:
                            return False, "kwargs['output'] must be json or xml"
                    else:
                        return False, "No results"
                except:
                    return False, None
            elif kwargs['doc_type'] and kwargs['doc_type'].lower() == "all":
                kwargs['dict']['Case']['Message'] = {'Attachments': {
                    'Attachment': kwargs['dict']['Case']['Message']['Attachments']['Attachment']}}
                if kwargs['output'] is not None and kwargs['output'].lower() == 'xml':
                    base64_xml = CaseSystem.to_xml(**kwargs)  # Data Conversion
                    return base64_xml, None
                elif kwargs['output'] is None or kwargs['output'].lower() == 'json':
                    base64_json = CaseSystem.to_json(**kwargs) # Data Conversion
                    return base64_json, None
                else:
                    return False, "kwargs['output'] must be json or xml"
            else:
                return False, "Use GET for all attachments..."
        if kwargs['request'].method == "GET":
            kwargs['dict']['Case']['Message'] = {'Attachments': {
                'Attachment': kwargs['dict']['Case']['Message']['Attachments']['Attachment']}}
            if kwargs['output'] is not None and kwargs['output'].lower() == 'xml':
                base64_xml = CaseSystem.to_xml(**kwargs)  # Data Conversion
                return base64_xml, None
            elif kwargs['output'] is None or kwargs['output'].lower() == 'json':
                base64_json = CaseSystem.to_json(**kwargs) # Data Conversio
                return base64_json, None
            else:
                return False, "kwargs['output'] must be json or xml"
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
        
        # Convert Xml or Json to python dict with the right codec from original file
        dict, msg = CaseSystem.convert_file_into_dict(
            file_type=file_type, xml_mime=xml_mime, file_enconding=file_enconding, json_mime=json_mime, **kwargs)

        # Attachment filter
        if (dict):
            if kwargs['attachment'] is None:
                result, msg = CaseSystem.case_with_all_attachment(dict=dict, file_enconding=file_enconding, **kwargs)
                return result, msg
            elif kwargs['attachment']:
                result, msg = CaseSystem.case_with_attachment_filter(dict=dict, file_enconding=file_enconding, **kwargs)
                return result, msg
            elif not kwargs['attachment']:
                result, msg = CaseSystem.case_without_attachment(dict=dict, file_enconding=file_enconding, **kwargs)
                return result, msg
        else:
            return False, msg
