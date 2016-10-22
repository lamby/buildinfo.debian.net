import datetime

from django.db import models

class Source(models.Model):
    name = models.CharField(max_length=200, unique=True)

    created = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('name',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u"pk=%d name=%r" % (
            self.pk,
            self.name,
        )

    @models.permalink
    def get_absolute_url(self):
        return 'packages:source', (self.name,)

class Binary(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u"pk=%d name=%r" % (
            self.pk,
            self.name,
        )

    @models.permalink
    def get_absolute_url(self):
        return 'packages:binary', (self.name,)

class Architecture(models.Model):
    name = models.CharField(max_length=200, unique=True)

    created = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('name',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u"pk=%d name=%r" % (
            self.pk,
            self.name,
        )
