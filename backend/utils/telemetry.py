import json
from threading import Thread
import requests
from urllib.parse import urljoin
from django.conf import settings

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
        
    def _post_request(self):
        r = requests.post(self.url, data=json.dumps(self.data))
        self.http_status_code = r.status_code
