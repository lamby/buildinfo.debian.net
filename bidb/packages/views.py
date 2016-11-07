from django.shortcuts import render, get_object_or_404

from bidb.utils.paginator import AutoPaginator

from .models import Binary, Source


def sources(request):
    page = AutoPaginator(request, Source.objects.all(), 250).current_page()

    return render(request, 'packages/sources.html', {
        'page': page,
    })

def binaries(request):
    page = AutoPaginator(request, Binary.objects.all(), 250).current_page()

    return render(request, 'packages/binaries.html', {
        'page': page,
    })


def source(request, name):
    source = get_object_or_404(Source, name=name)

    binaries = Binary.objects.filter(
        generated_binaries__buildinfo__source=source,
    ).distinct()

    versions = source.buildinfos.values_list('version', flat=True) \
        .order_by('version').distinct()

    return render(request, 'packages/source.html', {
        'source': source,
        'binaries': binaries,
        'versions': versions,
    })

def binary(request, name):
    binary = get_object_or_404(Binary, name=name)

    build_depends = binary.build_depends.select_related(
        'buildinfo__source',
        'buildinfo__architecture',
    ).order_by('buildinfo__source__name')

    versions = binary.generated_binaries.values_list(
        'buildinfo__version', flat=True,
    ).order_by('buildinfo__version').distinct()

    return render(request, 'packages/binary.html', {
        'binary': binary,
        'versions': versions,
        'build_depends': build_depends,
    })
