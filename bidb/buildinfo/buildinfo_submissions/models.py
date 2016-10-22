import datetime
import functools

from django.db import models
from django.utils.crypto import get_random_string


class Submission(models.Model):
    buildinfo = models.ForeignKey(
        'buildinfo.Buildinfo',
        related_name='submissions',
    )

    slug = models.CharField(
        unique=True,
        default=functools.partial(
            get_random_string, 8, '3479abcdefghijkmnopqrstuvwxyz',
        ),
        max_length=8,
    )

    uid = models.CharField(max_length=512)
    node = models.CharField(max_length=512)

    raw_text = models.TextField()

    created = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('created',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u"pk=%d buildinfo=%r" % (
            self.pk,
            self.buildinfo,
        )

    @models.permalink
    def get_absolute_url(self):
        return 'buildinfo:submissions:view', (
            self.buildinfo.sha1,
            self.buildinfo.get_filename(),
            self.slug,
        )
