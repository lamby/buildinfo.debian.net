import re
import hashlib

from debian import deb822

from django.db import IntegrityError

from bidb.packages.models import Source, Architecture, Binary
from bidb.buildinfo.models import Buildinfo

re_filename = re.compile(
    r'^(?P<name>[^_]+)_(?P<version>[^_]+)_(?P<architecture>[^\.]+)\.deb$',
)
re_installed_build_depends = re.compile(
    r'^(?P<package>[^ ]+) \(= (?P<version>.+)\)'
)


class InvalidSubmission(Exception):
    pass

def parse_submission(request):
    raw_text = request.read()

    data = deb822.Deb822(raw_text)
    raw_text_gpg_stripped = data.dump()

    # Parse GPG info
    uid = ''
    data.raw_text = raw_text
    gpg_info = data.get_gpg_info()
    if 'NODATA' not in gpg_info:
        try:
            uid = gpg_info['NO_PUBKEY'][0]
        except (KeyError, IndexError):
            raise InvalidBuildinfo("Could not determine GPG uid")

    sha1 = hashlib.sha1(raw_text_gpg_stripped.encode('utf-8')).hexdigest()
    try:
        submission = Buildinfo.objects.get(sha1=sha1).submissions.create(
            uid=uid,
            node=request.GET.get('node', ''),
            raw_text=raw_text,
        )

        return submission, False
    except Buildinfo.DoesNotExist:
        pass

    if data.get('Format') != '0.1':
        raise InvalidBuildinfo("Only Format: 1.0 is supported")

    def get_or_create(model, field):
        try:
            return model.objects.get_or_create(name=data[field])[0]
        except KeyError:
            raise InvalidBuildinfo("Missing required field: {}".format(field))

    buildinfo = Buildinfo.objects.create(
        sha1=sha1,
        raw_text=raw_text_gpg_stripped,

        source=get_or_create(Source, 'Source'),
        architecture=get_or_create(Architecture, 'Architecture'),
        version=data['Version'],

        build_path=data.get('Build-Path', ''),
        build_architecture=get_or_create(Architecture, 'Build-Architecture'),
    )

    ## Parse binaries #########################################################

    try:
        binary_names = set(data['Binary'].split(' '))
    except KeyError:
        raise InvalidBuildinfo("Missing 'Binary' field")

    if not binary_names:
        raise InvalidBuildinfo("Invalid 'Binary' field")

    binaries = {}
    for x in binary_names:
        # Save instances for lookup later
        binaries[x] = buildinfo.binaries.create(
            binary=Binary.objects.get_or_create(name=x)[0],
        )

    ## Parse checksums ########################################################

    hashes = ('Md5', 'Sha1', 'Sha256')

    checksums = {}
    for x in hashes:
        for y in data['Checksums-%s' % x].strip().splitlines():
            checksum, size, filename = y.strip().split()

            # Check filename
            if re_filename.match(filename) is None:
                raise InvalidBuildinfo("Invalid filename: {}".format(filename))

            # Check size
            try:
                size = int(size)
                if size < 0:
                    raise ValueError()
            except ValueError:
                raise InvalidBuildinfo(
                    "Invalid size for {}: {}".format(filename, size),
                )

            checksums.setdefault(filename, {
                'size': size,
            })['checksum_{}'.format(x.lower())] = checksum

            existing = checksums[filename]['size']
            if size != existing:
                raise InvalidBuildinfo("Mismatched file size in "
                    "Checksums-{}: {} != {}".format(x, existing, size))

    ## Create Binary instances ################################################

    for k, v in sorted(checksums.items()):
        try:
            v['binary'] = binaries[re_filename.match(k).group('name')]
        except KeyError:
            v['binary'] = None

        buildinfo.checksums.create(filename=k, **v)

    ## Create InstalledBuildDepends instances #################################

    for x in data['Installed-Build-Depends'].strip().splitlines():
        m = re_installed_build_depends.match(x.strip())

        binary = Binary.objects.get_or_create(name=m.group('package'))[0]

        buildinfo.installed_build_depends.get_or_create(
            binary=binary,
            version=m.group('version'),
        )

    return buildinfo.submissions.create(
        uid=uid,
        node=request.GET.get('node', ''),
        raw_text=raw_text,
    ), True
