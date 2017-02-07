from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.core.files.storage import default_storage

from .models import Submission


def view(request, sha1, filename, slug):
    submission = get_object_or_404(
        Submission,
        slug=slug,
        buildinfo__sha1=sha1,
    )

    if submission.buildinfo.get_filename() != filename:
        return redirect(submission)

    with default_storage.open(submission.get_storage_name()) as f:
        return HttpResponse(f, content_type='text/plain')
