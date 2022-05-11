from django.apps import AppConfig

import logging
log = logging.getLogger(__name__)


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):

        # This needs to be imported in order to
        # pick up all the registered rpc methods
        import backend.rpc
