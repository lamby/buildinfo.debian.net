from django.shortcuts import render

from bidb.buildinfo.models import Buildinfo

def landing(request):
    latest = Buildinfo.objects.all()[:10]

    return render(request, 'static/landing.html', {
        'latest': latest,
    })
