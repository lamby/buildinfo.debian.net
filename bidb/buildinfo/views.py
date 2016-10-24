from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Buildinfo


def view(request, sha1, filename=None):
    buildinfo = get_object_or_404(Buildinfo, sha1=sha1)

    if filename != buildinfo.get_filename():
        return redirect(buildinfo)

    installed_build_depends = buildinfo.installed_build_depends.select_related(
        'binary',
    )

    return render(request, 'buildinfo/view.html', {
        'buildinfo': buildinfo,
        'installed_build_depends': installed_build_depends,
    })

def raw_text(request, sha1, filename=None):
    buildinfo = get_object_or_404(Buildinfo, sha1=sha1)

    return HttpResponse(buildinfo.raw_text, content_type='text/plain')
