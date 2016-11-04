import celery
import subprocess

from bidb.utils.tempfile import TemporaryDirectory
from bidb.utils.subprocess import check_output2

from .models import Key


@celery.task(soft_time_limit=60)
def update_or_create_key(uid):
    with TemporaryDirectory() as homedir:
        try:
            check_output2((
                'gpg',
                '--homedir', homedir,
                '--keyserver', 'pgpkeys.mit.edu',
                '--recv-keys', uid,
            ))
        except subprocess.CalledProcessError as exc:
            print "E: {}: {}".format(exc, exc.output)
            return None, False

        data = check_output2((
            'gpg',
            '--homedir', homedir,
            '--with-colons',
            '--fixed-list-mode',
            '--fingerprint',
            uid,
        ))

    for line in data.splitlines():
        if line.startswith('uid:'):
            name = line.split(':')[9]
            break
    else:
        raise ValueError("Could not parse name from key: {}".format(data))

    return Key.objects.update_or_create(uid=uid, defaults={
        'name': name,
    })

@celery.task()
def refresh_all():
    for x in Key.objects.all():
        update_or_create_key.delay(x.uid)
