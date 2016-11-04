from django.core.management.base import NoArgsCommand

from ...tasks import update_or_create_key
from ...models import Key

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        for x in Key.objects.all():
            update_or_create_key.delay(x.uid)
