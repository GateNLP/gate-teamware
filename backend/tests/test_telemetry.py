from urllib.parse import urljoin

from django.test import TestCase
from django.conf import settings
import requests
import requests_mock

from backend.management.commands import load_test_fixture
from backend.utils.telemetry import TelemetrySender
from backend.models import Project

@requests_mock.Mocker()
class TestTelemetrySender(TestCase):

    def setUp(self):
        load_test_fixture.project_with_annotators()
        settings.TELEMETRY_ON = True
     
    def test_telemetry_sender(self, mocker):
        """Tests telemetry sender."""

        proj = Project.objects.first()

        ts = TelemetrySender("completed", {})

        mocker.post(ts.url, status_code=201) # set up mocker for http post request
        ts.send()
        assert ts.http_status_code == 201

        mocker.post(ts.url, status_code=500)
        ts.send()
        assert ts.http_status_code == 500


    def test_project_completion_telemetry(self, mocker):
        """Tests telemetry sending when project is completed."""

        url = urljoin(settings.TELEMETRY_BASE_URL, settings.TELEMETRY_PATH)
        mocker.post(url, status_code=201)

        proj = Project.objects.first()
        assert proj.is_completed

        proj.check_project_complete()

        # Assert that the http request was sent
        assert mocker.called == True

        # get the data that was sent
        sent_data = mocker.last_request.json()

        assert sent_data["product"] == "teamware"
        assert sent_data["status"] == "complete"
        assert sent_data["documents"] == 20
        assert sent_data["completed_tasks"] == 80


    def test_project_deletion_telemetry(self, mocker):
        """Tests telemetry sending when project is deleted."""
        
        url = urljoin(settings.TELEMETRY_BASE_URL, settings.TELEMETRY_PATH)
        mocker.post(url, status_code=201)

        proj = Project.objects.first()
        proj.delete()

        # Assert that the http request was sent
        assert mocker.called == True

        # get the data that was sent
        sent_data = mocker.last_request.json()

        assert sent_data["product"] == "teamware"
        assert sent_data["status"] == "deleted"
        assert sent_data["documents"] == 20

        # check that project is still deleted even if telemetry fails
        with self.assertRaises(Project.DoesNotExist): 
            Project.objects.get(id=proj.id)

@requests_mock.Mocker()
class TestFailingTelemetry(TestCase):

    def setUp(self):
        load_test_fixture.project_with_annotators()
        settings.TELEMETRY_ON = True
     
    def test_failing_telemetry(self, mocker):

        url = urljoin(settings.TELEMETRY_BASE_URL, settings.TELEMETRY_PATH) 

        # set up mocker for http post request with timeout
        mocker.post(url, exc=requests.exceptions.ConnectTimeout)

        proj = Project.objects.first()

        # delete a project, triggering a telemetry call
        with self.assertRaises(requests.exceptions.ConnectTimeout):
            proj.delete()

        # check that project is still deleted even if telemetry fails
        with self.assertRaises(Project.DoesNotExist): 
            Project.objects.get(id=proj.id)
