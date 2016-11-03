import celery
import subprocess

from bidb.utils.tempfile import TemporaryDirectory

from .models import Key


@celery.task(soft_time_limit=60)
def update_or_create_key(uid):
    with TemporaryDirectory() as homedir:
        subprocess.check_call((
            'gpg',
            '--homedir', homedir,
            '--keyserver', 'http://p80.pool.sks-keyservers.net/',
            '--recv-keys', uid
        ))

        data = subprocess.check_output((
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
