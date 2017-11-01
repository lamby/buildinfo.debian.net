from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.storage import default_storage

from .models import Buildinfo


def view(request, sha1, filename=None):
    buildinfo = get_object_or_404(Buildinfo, sha1=sha1)

    if filename != buildinfo.get_filename():
        return redirect(buildinfo)

    return render(request, 'buildinfo/view.html', {
        'buildinfo': buildinfo,
    })

def raw_text(request, sha1, filename=None):
    buildinfo = get_object_or_404(Buildinfo, sha1=sha1)

    with default_storage.open(buildinfo.get_storage_name()) as f:
        return HttpResponse(f, content_type='text/plain')

def checksums(request, sha1):
    buildinfo = Buildinfo.objects.filter(
        checksums__checksum_sha1=sha1,
    ).select_related(
        'source',
        'architecture',
    ).order_by()

    return JsonResponse({'buildinfos': [{
        'uri': '{}{}'.format(
            settings.SITE_URL,
            x.get_absolute_url(),
        ),
        'raw-uri': '{}{}'.format(
            settings.SITE_URL,
            x.get_absolute_raw_url(),
        ),
        'source': x.source.name,
        'version': x.version,
        'architecture': x.architecture.name,
    } for x in buildinfo]})
