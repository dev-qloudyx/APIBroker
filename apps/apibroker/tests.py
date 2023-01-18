from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from apps.apibroker.case import CaseSystem
from apps.apibroker.models import CaseInstanceManager, DmsBsmsInstanceManager
from apps.apibroker.views import CaseViewSet
from apps.knox.settings import CONSTANTS
from apps.users.models import User
from rest_framework import status
from rest_framework.test import APITestCase
#from apps.knox.models import AuthToken
from apps.knox.auth import AuthToken
from rest_framework.reverse import reverse
import base64
import codecs
class LoginTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='test@test.com', email='test@test.com', password='a123456789b')

    def test_login(self):
        # Encode the username and password
        auth = codecs.encode(f'test@test.com:a123456789b'.encode(), 'base64')
        auth = auth.strip()
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Basic {auth.decode()}'

        # Perform a login request
        response = self.client.post('/api/auth/login/')
        
        # Assert that the response has a status code of 200
        self.assertEqual(response.status_code, 200)

        # Assert that the response contains a token
        self.assertIn('Token', response.data)
        token = response.data['Token']
        

        auth_token = None

        try:
            auth_token = AuthToken.objects.filter(token_key=token[:CONSTANTS.TOKEN_KEY_LENGTH]).first()
            self.assertEqual(auth_token.user.username, self.user.username)
        except AuthToken.DoesNotExist as e:
            return f"{e}"

class CaseViewSetTest(APITestCase):
    # Test Case for calculation service
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test@test.com', email='test@test.com', password='a123456789b')
        #update user role
        User.objects.filter(pk=self.user.pk).update(role=19)
        #refresh user instance
        self.user.refresh_from_db()
        auth = codecs.encode(f'test@test.com:a123456789b'.encode(), 'base64')
        auth = auth.strip()
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Basic {auth.decode()}'
        
        self.valid_payload = {
            "originId": "COMPANY",
            "operatorId": "AF15295",
            "customerId": "COMPANY",
            "caseNumber":"123456789",
            "plateNumber":"PT-AX-99",
            "extReferenceNumber": "1A2X3F4H5A6D7G83R9",
            "caseFile":"PD94bWwgdmVyc2lvbj0iMS4wIj8+CjxjYXRhbG9nPgogICA8Ym9vayBpZD0iYmsxMDEiPgogICAgICA8YXV0aG9yPkdhbWJhcmRlbGxhLCBNYXR0aGV3PC9hdXRob3I+CiAgICAgIDx0aXRsZT5YTUwgRGV2ZWxvcGVyJ3MgR3VpZGU8L3RpdGxlPgogICAgICA8Z2VucmU+Q29tcHV0ZXI8L2dlbnJlPgogICAgICA8cHJpY2U+NDQuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDAtMTAtMDE8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPkFuIGluLWRlcHRoIGxvb2sgYXQgY3JlYXRpbmcgYXBwbGljYXRpb25zIAogICAgICB3aXRoIFhNTC48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazEwMiI+CiAgICAgIDxhdXRob3I+UmFsbHMsIEtpbTwvYXV0aG9yPgogICAgICA8dGl0bGU+TWlkbmlnaHQgUmFpbjwvdGl0bGU+CiAgICAgIDxnZW5yZT5GYW50YXN5PC9nZW5yZT4KICAgICAgPHByaWNlPjUuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDAtMTItMTY8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPkEgZm9ybWVyIGFyY2hpdGVjdCBiYXR0bGVzIGNvcnBvcmF0ZSB6b21iaWVzLCAKICAgICAgYW4gZXZpbCBzb3JjZXJlc3MsIGFuZCBoZXIgb3duIGNoaWxkaG9vZCB0byBiZWNvbWUgcXVlZW4gCiAgICAgIG9mIHRoZSB3b3JsZC48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazEwMyI+CiAgICAgIDxhdXRob3I+Q29yZXRzLCBFdmE8L2F1dGhvcj4KICAgICAgPHRpdGxlPk1hZXZlIEFzY2VuZGFudDwvdGl0bGU+CiAgICAgIDxnZW5yZT5GYW50YXN5PC9nZW5yZT4KICAgICAgPHByaWNlPjUuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDAtMTEtMTc8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPkFmdGVyIHRoZSBjb2xsYXBzZSBvZiBhIG5hbm90ZWNobm9sb2d5IAogICAgICBzb2NpZXR5IGluIEVuZ2xhbmQsIHRoZSB5b3VuZyBzdXJ2aXZvcnMgbGF5IHRoZSAKICAgICAgZm91bmRhdGlvbiBmb3IgYSBuZXcgc29jaWV0eS48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazEwNCI+CiAgICAgIDxhdXRob3I+Q29yZXRzLCBFdmE8L2F1dGhvcj4KICAgICAgPHRpdGxlPk9iZXJvbidzIExlZ2FjeTwvdGl0bGU+CiAgICAgIDxnZW5yZT5GYW50YXN5PC9nZW5yZT4KICAgICAgPHByaWNlPjUuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDEtMDMtMTA8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPkluIHBvc3QtYXBvY2FseXBzZSBFbmdsYW5kLCB0aGUgbXlzdGVyaW91cyAKICAgICAgYWdlbnQga25vd24gb25seSBhcyBPYmVyb24gaGVscHMgdG8gY3JlYXRlIGEgbmV3IGxpZmUgCiAgICAgIGZvciB0aGUgaW5oYWJpdGFudHMgb2YgTG9uZG9uLiBTZXF1ZWwgdG8gTWFldmUgCiAgICAgIEFzY2VuZGFudC48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazEwNSI+CiAgICAgIDxhdXRob3I+Q29yZXRzLCBFdmE8L2F1dGhvcj4KICAgICAgPHRpdGxlPlRoZSBTdW5kZXJlZCBHcmFpbDwvdGl0bGU+CiAgICAgIDxnZW5yZT5GYW50YXN5PC9nZW5yZT4KICAgICAgPHByaWNlPjUuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDEtMDktMTA8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPlRoZSB0d28gZGF1Z2h0ZXJzIG9mIE1hZXZlLCBoYWxmLXNpc3RlcnMsIAogICAgICBiYXR0bGUgb25lIGFub3RoZXIgZm9yIGNvbnRyb2wgb2YgRW5nbGFuZC4gU2VxdWVsIHRvIAogICAgICBPYmVyb24ncyBMZWdhY3kuPC9kZXNjcmlwdGlvbj4KICAgPC9ib29rPgogICA8Ym9vayBpZD0iYmsxMDYiPgogICAgICA8YXV0aG9yPlJhbmRhbGwsIEN5bnRoaWE8L2F1dGhvcj4KICAgICAgPHRpdGxlPkxvdmVyIEJpcmRzPC90aXRsZT4KICAgICAgPGdlbnJlPlJvbWFuY2U8L2dlbnJlPgogICAgICA8cHJpY2U+NC45NTwvcHJpY2U+CiAgICAgIDxwdWJsaXNoX2RhdGU+MjAwMC0wOS0wMjwvcHVibGlzaF9kYXRlPgogICAgICA8ZGVzY3JpcHRpb24+V2hlbiBDYXJsYSBtZWV0cyBQYXVsIGF0IGFuIG9ybml0aG9sb2d5IAogICAgICBjb25mZXJlbmNlLCB0ZW1wZXJzIGZseSBhcyBmZWF0aGVycyBnZXQgcnVmZmxlZC48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazEwNyI+CiAgICAgIDxhdXRob3I+VGh1cm1hbiwgUGF1bGE8L2F1dGhvcj4KICAgICAgPHRpdGxlPlNwbGlzaCBTcGxhc2g8L3RpdGxlPgogICAgICA8Z2VucmU+Um9tYW5jZTwvZ2VucmU+CiAgICAgIDxwcmljZT40Ljk1PC9wcmljZT4KICAgICAgPHB1Ymxpc2hfZGF0ZT4yMDAwLTExLTAyPC9wdWJsaXNoX2RhdGU+CiAgICAgIDxkZXNjcmlwdGlvbj5BIGRlZXAgc2VhIGRpdmVyIGZpbmRzIHRydWUgbG92ZSB0d2VudHkgCiAgICAgIHRob3VzYW5kIGxlYWd1ZXMgYmVuZWF0aCB0aGUgc2VhLjwvZGVzY3JpcHRpb24+CiAgIDwvYm9vaz4KICAgPGJvb2sgaWQ9ImJrMTA4Ij4KICAgICAgPGF1dGhvcj5Lbm9yciwgU3RlZmFuPC9hdXRob3I+CiAgICAgIDx0aXRsZT5DcmVlcHkgQ3Jhd2xpZXM8L3RpdGxlPgogICAgICA8Z2VucmU+SG9ycm9yPC9nZW5yZT4KICAgICAgPHByaWNlPjQuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDAtMTItMDY8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPkFuIGFudGhvbG9neSBvZiBob3Jyb3Igc3RvcmllcyBhYm91dCByb2FjaGVzLAogICAgICBjZW50aXBlZGVzLCBzY29ycGlvbnMgIGFuZCBvdGhlciBpbnNlY3RzLjwvZGVzY3JpcHRpb24+CiAgIDwvYm9vaz4KICAgPGJvb2sgaWQ9ImJrMTA5Ij4KICAgICAgPGF1dGhvcj5LcmVzcywgUGV0ZXI8L2F1dGhvcj4KICAgICAgPHRpdGxlPlBhcmFkb3ggTG9zdDwvdGl0bGU+CiAgICAgIDxnZW5yZT5TY2llbmNlIEZpY3Rpb248L2dlbnJlPgogICAgICA8cHJpY2U+Ni45NTwvcHJpY2U+CiAgICAgIDxwdWJsaXNoX2RhdGU+MjAwMC0xMS0wMjwvcHVibGlzaF9kYXRlPgogICAgICA8ZGVzY3JpcHRpb24+QWZ0ZXIgYW4gaW5hZHZlcnRhbnQgdHJpcCB0aHJvdWdoIGEgSGVpc2VuYmVyZwogICAgICBVbmNlcnRhaW50eSBEZXZpY2UsIEphbWVzIFNhbHdheSBkaXNjb3ZlcnMgdGhlIHByb2JsZW1zIAogICAgICBvZiBiZWluZyBxdWFudHVtLjwvZGVzY3JpcHRpb24+CiAgIDwvYm9vaz4KICAgPGJvb2sgaWQ9ImJrMTEwIj4KICAgICAgPGF1dGhvcj5PJ0JyaWVuLCBUaW08L2F1dGhvcj4KICAgICAgPHRpdGxlPk1pY3Jvc29mdCAuTkVUOiBUaGUgUHJvZ3JhbW1pbmcgQmlibGU8L3RpdGxlPgogICAgICA8Z2VucmU+Q29tcHV0ZXI8L2dlbnJlPgogICAgICA8cHJpY2U+MzYuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDAtMTItMDk8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPk1pY3Jvc29mdCdzIC5ORVQgaW5pdGlhdGl2ZSBpcyBleHBsb3JlZCBpbiAKICAgICAgZGV0YWlsIGluIHRoaXMgZGVlcCBwcm9ncmFtbWVyJ3MgcmVmZXJlbmNlLjwvZGVzY3JpcHRpb24+CiAgIDwvYm9vaz4KICAgPGJvb2sgaWQ9ImJrMTExIj4KICAgICAgPGF1dGhvcj5PJ0JyaWVuLCBUaW08L2F1dGhvcj4KICAgICAgPHRpdGxlPk1TWE1MMzogQSBDb21wcmVoZW5zaXZlIEd1aWRlPC90aXRsZT4KICAgICAgPGdlbnJlPkNvbXB1dGVyPC9nZW5yZT4KICAgICAgPHByaWNlPjM2Ljk1PC9wcmljZT4KICAgICAgPHB1Ymxpc2hfZGF0ZT4yMDAwLTEyLTAxPC9wdWJsaXNoX2RhdGU+CiAgICAgIDxkZXNjcmlwdGlvbj5UaGUgTWljcm9zb2Z0IE1TWE1MMyBwYXJzZXIgaXMgY292ZXJlZCBpbiAKICAgICAgZGV0YWlsLCB3aXRoIGF0dGVudGlvbiB0byBYTUwgRE9NIGludGVyZmFjZXMsIFhTTFQgcHJvY2Vzc2luZywgCiAgICAgIFNBWCBhbmQgbW9yZS48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazExMiI+CiAgICAgIDxhdXRob3I+R2Fsb3MsIE1pa2U8L2F1dGhvcj4KICAgICAgPHRpdGxlPlZpc3VhbCBTdHVkaW8gNzogQSBDb21wcmVoZW5zaXZlIEd1aWRlPC90aXRsZT4KICAgICAgPGdlbnJlPkNvbXB1dGVyPC9nZW5yZT4KICAgICAgPHByaWNlPjQ5Ljk1PC9wcmljZT4KICAgICAgPHB1Ymxpc2hfZGF0ZT4yMDAxLTA0LTE2PC9wdWJsaXNoX2RhdGU+CiAgICAgIDxkZXNjcmlwdGlvbj5NaWNyb3NvZnQgVmlzdWFsIFN0dWRpbyA3IGlzIGV4cGxvcmVkIGluIGRlcHRoLAogICAgICBsb29raW5nIGF0IGhvdyBWaXN1YWwgQmFzaWMsIFZpc3VhbCBDKyssIEMjLCBhbmQgQVNQKyBhcmUgCiAgICAgIGludGVncmF0ZWQgaW50byBhIGNvbXByZWhlbnNpdmUgZGV2ZWxvcG1lbnQgCiAgICAgIGVudmlyb25tZW50LjwvZGVzY3JpcHRpb24+CiAgIDwvYm9vaz4KPC9jYXRhbG9nPg=="
        }
        self.invalid_payload = {
            'caseFile': 'not_base64',
            'caseNumber': '',
            'customerId': '',
            'plateNumber': ''
        }
        self.url = '/api/sendcase/'


    def test_create_valid_case(self):
        response_token = self.client.post('/api/auth/login/')
        token = response_token.data['Token']
        response_sendcase = self.client.post(self.url, data=self.valid_payload, HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(response_sendcase.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_sendcase.data['resultCode'], 1)

    def test_create_invalid_case(self):
        # Get token
        response_token = self.client.post('/api/auth/login/')
        token = response_token.data['Token']
        # Send invalid payload
        response = self.client.post(self.url, data=self.invalid_payload, HTTP_AUTHORIZATION=f'Token {token}')

        # Assert that the response has a status code of 400
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the resource is not created
        self.assertFalse(CaseInstanceManager.objects.filter(caseNumber=self.invalid_payload['caseNumber'], customerId=self.invalid_payload['customerId'], plateNumber=self.invalid_payload['plateNumber']).exists())

        # Check the response body for specific error messages or validation errors
        self.assertIn('errorDescription', response.data)
        self.assertIn('plateNumber', response.data['errorDescription'])
        self.assertEqual(response.data['errorDescription']['plateNumber'][0], 'This field may not be blank.')

    def test_authentication_required(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
class CaseListViewTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username='test@test.com',email='test@test.com', password='a123456789b')
         
        # update user role and associate user to an dmsbsms
        DmsBsmsInstanceManager.objects.create(originId='COMPANY', operatorId='AF15295', customerId='COMPANY', owner=self.user)
        User.objects.filter(pk=self.user.pk).update(role=29)
    
        # refresh user instance
        self.user.refresh_from_db()
        auth = codecs.encode(f'test@test.com:a123456789b'.encode(), 'base64')
        auth = auth.strip()
        self.client.defaults['HTTP_AUTHORIZATION'] = f'Basic {auth.decode()}'
        
        self.valid_payload = {
            "originId": "COMPANY",
            "operatorId": "AF15295",
            "customerId": "COMPANY",
            "caseNumber":"123456789",
            "plateNumber":"PT-AX-99",
            "extReferenceNumber": "1A2X3F4H5A6D7G83R9",
            "binary":b"PD94bWwgdmVyc2lvbj0iMS4wIj8+CjxjYXRhbG9nPgogICA8Ym9vayBpZD0iYmsxMDEiPgogICAgICA8YXV0aG9yPkdhbWJhcmRlbGxhLCBNYXR0aGV3PC9hdXRob3I+CiAgICAgIDx0aXRsZT5YTUwgRGV2ZWxvcGVyJ3MgR3VpZGU8L3RpdGxlPgogICAgICA8Z2VucmU+Q29tcHV0ZXI8L2dlbnJlPgogICAgICA8cHJpY2U+NDQuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDAtMTAtMDE8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPkFuIGluLWRlcHRoIGxvb2sgYXQgY3JlYXRpbmcgYXBwbGljYXRpb25zIAogICAgICB3aXRoIFhNTC48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazEwMiI+CiAgICAgIDxhdXRob3I+UmFsbHMsIEtpbTwvYXV0aG9yPgogICAgICA8dGl0bGU+TWlkbmlnaHQgUmFpbjwvdGl0bGU+CiAgICAgIDxnZW5yZT5GYW50YXN5PC9nZW5yZT4KICAgICAgPHByaWNlPjUuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDAtMTItMTY8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPkEgZm9ybWVyIGFyY2hpdGVjdCBiYXR0bGVzIGNvcnBvcmF0ZSB6b21iaWVzLCAKICAgICAgYW4gZXZpbCBzb3JjZXJlc3MsIGFuZCBoZXIgb3duIGNoaWxkaG9vZCB0byBiZWNvbWUgcXVlZW4gCiAgICAgIG9mIHRoZSB3b3JsZC48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazEwMyI+CiAgICAgIDxhdXRob3I+Q29yZXRzLCBFdmE8L2F1dGhvcj4KICAgICAgPHRpdGxlPk1hZXZlIEFzY2VuZGFudDwvdGl0bGU+CiAgICAgIDxnZW5yZT5GYW50YXN5PC9nZW5yZT4KICAgICAgPHByaWNlPjUuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDAtMTEtMTc8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPkFmdGVyIHRoZSBjb2xsYXBzZSBvZiBhIG5hbm90ZWNobm9sb2d5IAogICAgICBzb2NpZXR5IGluIEVuZ2xhbmQsIHRoZSB5b3VuZyBzdXJ2aXZvcnMgbGF5IHRoZSAKICAgICAgZm91bmRhdGlvbiBmb3IgYSBuZXcgc29jaWV0eS48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazEwNCI+CiAgICAgIDxhdXRob3I+Q29yZXRzLCBFdmE8L2F1dGhvcj4KICAgICAgPHRpdGxlPk9iZXJvbidzIExlZ2FjeTwvdGl0bGU+CiAgICAgIDxnZW5yZT5GYW50YXN5PC9nZW5yZT4KICAgICAgPHByaWNlPjUuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDEtMDMtMTA8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPkluIHBvc3QtYXBvY2FseXBzZSBFbmdsYW5kLCB0aGUgbXlzdGVyaW91cyAKICAgICAgYWdlbnQga25vd24gb25seSBhcyBPYmVyb24gaGVscHMgdG8gY3JlYXRlIGEgbmV3IGxpZmUgCiAgICAgIGZvciB0aGUgaW5oYWJpdGFudHMgb2YgTG9uZG9uLiBTZXF1ZWwgdG8gTWFldmUgCiAgICAgIEFzY2VuZGFudC48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazEwNSI+CiAgICAgIDxhdXRob3I+Q29yZXRzLCBFdmE8L2F1dGhvcj4KICAgICAgPHRpdGxlPlRoZSBTdW5kZXJlZCBHcmFpbDwvdGl0bGU+CiAgICAgIDxnZW5yZT5GYW50YXN5PC9nZW5yZT4KICAgICAgPHByaWNlPjUuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDEtMDktMTA8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPlRoZSB0d28gZGF1Z2h0ZXJzIG9mIE1hZXZlLCBoYWxmLXNpc3RlcnMsIAogICAgICBiYXR0bGUgb25lIGFub3RoZXIgZm9yIGNvbnRyb2wgb2YgRW5nbGFuZC4gU2VxdWVsIHRvIAogICAgICBPYmVyb24ncyBMZWdhY3kuPC9kZXNjcmlwdGlvbj4KICAgPC9ib29rPgogICA8Ym9vayBpZD0iYmsxMDYiPgogICAgICA8YXV0aG9yPlJhbmRhbGwsIEN5bnRoaWE8L2F1dGhvcj4KICAgICAgPHRpdGxlPkxvdmVyIEJpcmRzPC90aXRsZT4KICAgICAgPGdlbnJlPlJvbWFuY2U8L2dlbnJlPgogICAgICA8cHJpY2U+NC45NTwvcHJpY2U+CiAgICAgIDxwdWJsaXNoX2RhdGU+MjAwMC0wOS0wMjwvcHVibGlzaF9kYXRlPgogICAgICA8ZGVzY3JpcHRpb24+V2hlbiBDYXJsYSBtZWV0cyBQYXVsIGF0IGFuIG9ybml0aG9sb2d5IAogICAgICBjb25mZXJlbmNlLCB0ZW1wZXJzIGZseSBhcyBmZWF0aGVycyBnZXQgcnVmZmxlZC48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazEwNyI+CiAgICAgIDxhdXRob3I+VGh1cm1hbiwgUGF1bGE8L2F1dGhvcj4KICAgICAgPHRpdGxlPlNwbGlzaCBTcGxhc2g8L3RpdGxlPgogICAgICA8Z2VucmU+Um9tYW5jZTwvZ2VucmU+CiAgICAgIDxwcmljZT40Ljk1PC9wcmljZT4KICAgICAgPHB1Ymxpc2hfZGF0ZT4yMDAwLTExLTAyPC9wdWJsaXNoX2RhdGU+CiAgICAgIDxkZXNjcmlwdGlvbj5BIGRlZXAgc2VhIGRpdmVyIGZpbmRzIHRydWUgbG92ZSB0d2VudHkgCiAgICAgIHRob3VzYW5kIGxlYWd1ZXMgYmVuZWF0aCB0aGUgc2VhLjwvZGVzY3JpcHRpb24+CiAgIDwvYm9vaz4KICAgPGJvb2sgaWQ9ImJrMTA4Ij4KICAgICAgPGF1dGhvcj5Lbm9yciwgU3RlZmFuPC9hdXRob3I+CiAgICAgIDx0aXRsZT5DcmVlcHkgQ3Jhd2xpZXM8L3RpdGxlPgogICAgICA8Z2VucmU+SG9ycm9yPC9nZW5yZT4KICAgICAgPHByaWNlPjQuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDAtMTItMDY8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPkFuIGFudGhvbG9neSBvZiBob3Jyb3Igc3RvcmllcyBhYm91dCByb2FjaGVzLAogICAgICBjZW50aXBlZGVzLCBzY29ycGlvbnMgIGFuZCBvdGhlciBpbnNlY3RzLjwvZGVzY3JpcHRpb24+CiAgIDwvYm9vaz4KICAgPGJvb2sgaWQ9ImJrMTA5Ij4KICAgICAgPGF1dGhvcj5LcmVzcywgUGV0ZXI8L2F1dGhvcj4KICAgICAgPHRpdGxlPlBhcmFkb3ggTG9zdDwvdGl0bGU+CiAgICAgIDxnZW5yZT5TY2llbmNlIEZpY3Rpb248L2dlbnJlPgogICAgICA8cHJpY2U+Ni45NTwvcHJpY2U+CiAgICAgIDxwdWJsaXNoX2RhdGU+MjAwMC0xMS0wMjwvcHVibGlzaF9kYXRlPgogICAgICA8ZGVzY3JpcHRpb24+QWZ0ZXIgYW4gaW5hZHZlcnRhbnQgdHJpcCB0aHJvdWdoIGEgSGVpc2VuYmVyZwogICAgICBVbmNlcnRhaW50eSBEZXZpY2UsIEphbWVzIFNhbHdheSBkaXNjb3ZlcnMgdGhlIHByb2JsZW1zIAogICAgICBvZiBiZWluZyBxdWFudHVtLjwvZGVzY3JpcHRpb24+CiAgIDwvYm9vaz4KICAgPGJvb2sgaWQ9ImJrMTEwIj4KICAgICAgPGF1dGhvcj5PJ0JyaWVuLCBUaW08L2F1dGhvcj4KICAgICAgPHRpdGxlPk1pY3Jvc29mdCAuTkVUOiBUaGUgUHJvZ3JhbW1pbmcgQmlibGU8L3RpdGxlPgogICAgICA8Z2VucmU+Q29tcHV0ZXI8L2dlbnJlPgogICAgICA8cHJpY2U+MzYuOTU8L3ByaWNlPgogICAgICA8cHVibGlzaF9kYXRlPjIwMDAtMTItMDk8L3B1Ymxpc2hfZGF0ZT4KICAgICAgPGRlc2NyaXB0aW9uPk1pY3Jvc29mdCdzIC5ORVQgaW5pdGlhdGl2ZSBpcyBleHBsb3JlZCBpbiAKICAgICAgZGV0YWlsIGluIHRoaXMgZGVlcCBwcm9ncmFtbWVyJ3MgcmVmZXJlbmNlLjwvZGVzY3JpcHRpb24+CiAgIDwvYm9vaz4KICAgPGJvb2sgaWQ9ImJrMTExIj4KICAgICAgPGF1dGhvcj5PJ0JyaWVuLCBUaW08L2F1dGhvcj4KICAgICAgPHRpdGxlPk1TWE1MMzogQSBDb21wcmVoZW5zaXZlIEd1aWRlPC90aXRsZT4KICAgICAgPGdlbnJlPkNvbXB1dGVyPC9nZW5yZT4KICAgICAgPHByaWNlPjM2Ljk1PC9wcmljZT4KICAgICAgPHB1Ymxpc2hfZGF0ZT4yMDAwLTEyLTAxPC9wdWJsaXNoX2RhdGU+CiAgICAgIDxkZXNjcmlwdGlvbj5UaGUgTWljcm9zb2Z0IE1TWE1MMyBwYXJzZXIgaXMgY292ZXJlZCBpbiAKICAgICAgZGV0YWlsLCB3aXRoIGF0dGVudGlvbiB0byBYTUwgRE9NIGludGVyZmFjZXMsIFhTTFQgcHJvY2Vzc2luZywgCiAgICAgIFNBWCBhbmQgbW9yZS48L2Rlc2NyaXB0aW9uPgogICA8L2Jvb2s+CiAgIDxib29rIGlkPSJiazExMiI+CiAgICAgIDxhdXRob3I+R2Fsb3MsIE1pa2U8L2F1dGhvcj4KICAgICAgPHRpdGxlPlZpc3VhbCBTdHVkaW8gNzogQSBDb21wcmVoZW5zaXZlIEd1aWRlPC90aXRsZT4KICAgICAgPGdlbnJlPkNvbXB1dGVyPC9nZW5yZT4KICAgICAgPHByaWNlPjQ5Ljk1PC9wcmljZT4KICAgICAgPHB1Ymxpc2hfZGF0ZT4yMDAxLTA0LTE2PC9wdWJsaXNoX2RhdGU+CiAgICAgIDxkZXNjcmlwdGlvbj5NaWNyb3NvZnQgVmlzdWFsIFN0dWRpbyA3IGlzIGV4cGxvcmVkIGluIGRlcHRoLAogICAgICBsb29raW5nIGF0IGhvdyBWaXN1YWwgQmFzaWMsIFZpc3VhbCBDKyssIEMjLCBhbmQgQVNQKyBhcmUgCiAgICAgIGludGVncmF0ZWQgaW50byBhIGNvbXByZWhlbnNpdmUgZGV2ZWxvcG1lbnQgCiAgICAgIGVudmlyb25tZW50LjwvZGVzY3JpcHRpb24+CiAgIDwvYm9vaz4KPC9jYXRhbG9nPg=="
        }
        self.case = CaseInstanceManager.objects.create(owner=self.user, **self.valid_payload)
        
    def test_list_cases_success(self):
        response_token = self.client.post('/api/auth/login/')
        token = response_token.data['Token']
        request = self.factory.get('/api/getcase/', HTTP_AUTHORIZATION=f'Token {token}')
        request.user = self.user
        view = CaseViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['resultCode'], 1)
        self.assertEqual(len(response.data['Result']), 1)
        self.assertEqual(response.data['Result'][0]['owner'], 'test@test.com')

    def test_list_cases_no_cases(self):
        response_token = self.client.post('/api/auth/login/')
        token = response_token.data['Token']
        request = self.factory.get('/api/getcase/', HTTP_AUTHORIZATION=f'Token {token}')
        request.user = self.user
        CaseInstanceManager.objects.all().delete()
        view = CaseViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['resultCode'], 0)
        self.assertEqual(response.data['errorDescription'], ['No cases available'])