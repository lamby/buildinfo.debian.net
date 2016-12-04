import datetime

from django.db import models


class Buildinfo(models.Model):
    sha1 = models.CharField(max_length=40, unique=True)

    source = models.ForeignKey(
        'packages.Source',
        related_name='buildinfos',
    )

    architecture = models.ForeignKey(
        'packages.Architecture',
        related_name='buildinfos',
    )
    version = models.CharField(max_length=200)

    build_path = models.CharField(max_length=512)
    build_date = models.DateTimeField(null=True)
    build_origin = models.ForeignKey('Origin', null=True)
    build_architecture = models.ForeignKey(
        'packages.Architecture',
        related_name='buildinfos_build',
    )

    environment = models.TextField()

    raw_text = models.TextField()

    created = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u"pk=%d source=%r" % (
            self.pk,
            self.source,
        )

    @models.permalink
    def get_absolute_url(self):
        return 'buildinfo:view', (self.sha1, self.get_filename())

    def get_filename(self):
        return '{}_{}_{}'.format(
            self.source.name,
            self.version,
            self.architecture.name,
        )

class Binary(models.Model):
    buildinfo = models.ForeignKey(
        Buildinfo,
        related_name='binaries',
    )

    binary = models.ForeignKey(
        'packages.Binary',
        related_name='generated_binaries',
    )

    created = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('binary__name',)
        get_latest_by = 'created'
        unique_together = (
            ('buildinfo', 'binary'),
        )

    def __unicode__(self):
        return u"pk=%d binary=%r" % (
            self.pk,
            self.binary,
        )

class Checksum(models.Model):
    """
    Not the same as Binary as we could potentially have a Checksum for a
    Binary, etc.
    """

    buildinfo = models.ForeignKey(Buildinfo, related_name='checksums')

    filename = models.CharField(max_length=255)
    size = models.IntegerField()

    checksum_md5 = models.CharField(max_length=100)
    checksum_sha1 = models.CharField(max_length=100)
    checksum_sha256 = models.CharField(max_length=100)

    binary = models.OneToOneField(Binary, null=True, related_name='checksum')

    created = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('-created',)
        get_latest_by = 'created'
        unique_together = (
            ('buildinfo', 'filename'),
        )

    def __unicode__(self):
        return u"pk=%d filename=%r" % (
            self.pk,
            self.filename,
        )

class Origin(models.Model):
    name = models.CharField(max_length=255)

    created = models.DateTimeField(default=datetime.datetime.utcnow)

    class Meta:
        ordering = ('name',)
        get_latest_by = 'created'

    def __unicode__(self):
        return u"pk=%d name=%r" % (
            self.pk,
            self.name,
        )

class InstalledBuildDepends(models.Model):
    buildinfo = models.ForeignKey(
        Buildinfo,
        related_name='installed_build_depends',
    )

    binary = models.ForeignKey(
        'packages.Binary',
        related_name='build_depends',
    )

    version = models.CharField(max_length=200)

    class Meta:
        ordering = ('binary__name',)
        get_latest_by = 'created'
        unique_together = (
            ('buildinfo', 'binary'),
        )

    def __unicode__(self):
        return u"pk=%d buildinfo=%r binary=%r version=%r" % (
            self.pk,
            self.buildinfo,
            self.binary,
            self.version,
        )
