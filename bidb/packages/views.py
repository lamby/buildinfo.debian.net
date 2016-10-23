from django.shortcuts import render, get_object_or_404

from bidb.utils.paginator import AutoPaginator

from .models import Binary, Source


def sources(request):
    page = AutoPaginator(request, Source.objects.all(), 250).current_page()

    return render(request, 'packages/sources.html', {
        'page': page,
    })

def source(request, name):
    source = get_object_or_404(Source, name=name)

    return render(request, 'packages/source.html', {
        'source': source,
    })

def binary(request, name):
    binary = get_object_or_404(Binary, name=name)

    return render(request, 'packages/binary.html', {
        'binary': binary,
    })
