from django.http import HttpResponse
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
