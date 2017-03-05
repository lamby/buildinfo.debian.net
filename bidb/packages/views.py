from django.http import Http404
from django.shortcuts import render, get_object_or_404

from bidb.utils.itertools import groupby
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

def source_version(request, name, version):
    source = get_object_or_404(Source, name=name)

    if not source.buildinfos.filter(version=version).exists():
        raise Http404()

    qs = source.buildinfos.filter(
        version=version,
    ).order_by(
        'architecture__name',
    ).prefetch_related(
        'submissions__key',
    )

    buildinfos_by_arch = groupby(
        qs,
        lambda x: x.architecture.name,
        lambda x: x.created,
    )

    reproducible_by_arch = {}
    for x, ys in buildinfos_by_arch:
        checksums = {
            z.filename: z.checksum_sha256
            for y in ys
            for z in y.checksums.all()
        }

        reproducible = True
        for y in ys:
            for z in y.checksums.all():
                if checksums[z.filename] != z.checksum_sha256:
                    reproducible = False

        reproducible_by_arch[x] = reproducible

    return render(request, 'packages/source_version.html', {
        'source': source,
        'version': version,
        'buildinfos_by_arch': buildinfos_by_arch,
        'reproducible_by_arch': reproducible_by_arch,
    })

def binary(request, name):
    binary = get_object_or_404(Binary, name=name)

    versions = binary.generated_binaries.values_list(
        'buildinfo__version', flat=True,
    ).order_by('buildinfo__version').distinct()

    return render(request, 'packages/binary.html', {
        'binary': binary,
        'versions': versions,
    })
