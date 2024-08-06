from django.apps import AppConfig


class DjangocouchappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djangocouchapp'

from cloudant.client import Cloudant, CouchDB

class ReviewsConfig(AppConfig):
    name = 'reviews'

    def ready(self):
        from django.conf import settings
        self.client = CouchDB("admin", "admin", url='http://127.0.0.1:5984', connect=True)
        self.db = self.client.create_database(settings.CLOUDANT['grupo10'], throw_on_exists=False)
