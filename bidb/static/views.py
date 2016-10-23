from django.shortcuts import render

from bidb.buildinfo.buildinfo_submissions.models import Submission

def landing(request):
    latest = Submission.objects.all()[:20]

    return render(request, 'static/landing.html', {
        'latest': latest,
    })
