import datetime

from django.db import models, transaction


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

    def save(self, *args, **kwargs):
        created = not self.pk

        super(Key, self).save(*args, **kwargs)

        if created:
            from .tasks import update_or_create_key

            transaction.on_commit(lambda: update_or_create_key.delay(self.uid))
