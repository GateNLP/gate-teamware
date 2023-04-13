import json
import logging
from threading import Thread
import requests
from urllib.parse import urljoin
from django.conf import settings

log = logging.getLogger(__name__)
class TelemetrySender:

    def __init__(self, status: str, data: dict) -> None:
        self.url = urljoin(settings.TELEMETRY_BASE_URL, settings.TELEMETRY_PATH)
        self.data = data
        self.data.update({"product": "teamware", "status": status})
        self.http_status_code = None

    def send(self):
        """
        Makes a post request to the telemetry server containing a dict as json data, if telemetry is switched on.
        """
        
        if settings.TELEMETRY_ON:
            self.thread = Thread(target=self._post_request)
            self.thread.run()
        else:
            log.info(f"Telemetry is switched off. Not sending telemetry data for project {self.data['uuid']}.")
        
    def _post_request(self):
        log.info(f"Sending telemetry data for project {self.data['uuid']} to {self.url}.")
        r = requests.post(self.url, json=self.data)
        self.http_status_code = r.status_code
        log.info(f"{self.http_status_code}: {r.text}")
