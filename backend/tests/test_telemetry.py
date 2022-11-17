from django.test import TestCase
from backend.management.commands import load_test_fixture
from backend.utils.telemetry import TelemetrySender
import requests_mock

class TestTelemetrySender(TestCase):

    def setUp(self):
        load_test_fixture.create_db_users_with_project_and_annotation()
     
    @requests_mock.Mocker()
    def test_telemetry_sender(self, m):
        
        ts = TelemetrySender()
        assert ts.previous_call == None # No previous calls

        assert ts.data['new_annotators'] == 3
        assert ts.data['new_projects'] == 1
        assert ts.data['new_documents'] == 20

        m.post(ts.url, status_code=201) # set up mocker for http post request
        ts.send()
        assert ts.db_entry.status == 201


        

