from django.db import transaction
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from bidb.buildinfo.models import Buildinfo
from bidb.buildinfo.buildinfo_submissions.models import Submission

class Command(BaseCommand):
    def handle(self, **options):
        print "Migrating buildinfo.Buildinfo"
        for x in Buildinfo.objects.exclude(raw_text=''):
            self.handle_instance(x)

        print "Migrating buildinfo_submissions.Submission"
        for x in Submission.objects.exclude(raw_text=''):
            self.handle_instance(x)

    @transaction.atomic
    def handle_instance(self, x):
        print "Saving to {}".format(x.get_storage_name())
        default_storage.save(x.get_storage_name(), ContentFile(x.raw_text))
        x.raw_text = ''
        x.save(update_fields=('raw_text',))
