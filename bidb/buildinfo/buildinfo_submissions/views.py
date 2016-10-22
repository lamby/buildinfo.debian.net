from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404

from .models import Submission


def view(request, sha1, filename, slug):
    submission = get_object_or_404(
        Submission,
        slug=slug,
        buildinfo__sha1=sha1,
    )

    if submission.buildinfo.get_filename() != filename:
        return redirect(submission)

    return HttpResponse(submission.raw_text, content_type='text/plain')
