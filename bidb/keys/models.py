import datetime

from django.db import models


class Key(models.Model):
    uid = models.CharField(max_length=255, unique=True)

    name = models.TextField()

    created = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u"pk=%d uid=%r name=%r" % (
            self.pk,
            self.uid,
            self.name,
        )
