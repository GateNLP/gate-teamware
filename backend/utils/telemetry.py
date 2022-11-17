import datetime
import json
import requests
from urllib.parse import urljoin
from django.conf import settings
from backend.models import Document, Project, ServiceUser, Telemetry
import django.db

class TelemetrySender:

    def __init__(self) -> None:
        self.url = urljoin(settings.TELEMETRY_BASE_URL, settings.TELEMETRY_PATH)
        self.previous_call = self._get_previous_call()
        self.data = self._collect_data()
        self.db_entry = None

    def _collect_data(self) -> dict:
        """
        Collects the data to be sent to the telemetry server.
        """
        data = {}
        data['new_annotators'] = self._collect_new(ServiceUser)
        data['new_projects'] = self._collect_new(Project)
        data['new_documents'] = self._collect_new(Document)
        return data

    def _collect_new(self, model: django.db.models.Model) -> int:
        """
        Collects new database entries since the last successful telemetry call.
        """

        if self.previous_call is None: # If there is no previous call, count everything
            return model.objects.all().count()
        else:
            return model.objects.filter(created__lt=self.previous_call).count()

    def send(self) -> int:
        """
        Makes a post request to the telemetry server containing a dict as json data.
        """
        
        r = requests.post(self.url, data=json.dumps(self.data))

        self.db_entry = self._log_telemetry_call(r.status_code, self.data)

        return r.status_code

    def _log_telemetry_call(self, status: int, data:dict) -> Telemetry:
        """
        Logs a telemetry call attempt to the database.

        Returns:
            t (int): Telemetry instance added to the database
        """

        t = Telemetry.objects.create(
            data=data,
            status=status
        )
        t.save()
        return t

    def _get_previous_call(self) -> datetime.datetime:
        """
        Gets the last time there was a successful telemetry call.
        """
        call = Telemetry.objects.filter(status=201).last()
        
        if call is None:
            return None
        else:
            return call.sent