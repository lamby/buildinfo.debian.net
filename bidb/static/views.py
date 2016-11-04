from django.shortcuts import render

from bidb.buildinfo.buildinfo_submissions.models import Submission

def landing(request):
    latest = Submission.objects.select_related('key').order_by('-created')[:20]
    num_submissions = Submission.objects.count()

    return render(request, 'static/landing.html', {
        'latest': latest,
        'num_submissions': num_submissions,
    })
