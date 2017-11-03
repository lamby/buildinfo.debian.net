from django.conf import settings
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404

from bidb.utils.itertools import groupby
from bidb.utils.paginator import AutoPaginator

from bidb.buildinfo.buildinfo_submissions.models import Submission

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


def api_source_version_architecture(request, name, version, architecture):
    source = get_object_or_404(Source, name=name)

    if not source.buildinfos.filter(version=version).exists():
        raise Http404()

    qs = Submission.objects.filter(
        buildinfo__version=version,
        buildinfo__source_id=source,
        buildinfo__architecture__name=architecture,
    ).select_related(
        'key',
        'buildinfo',
        'buildinfo__architecture',
        'buildinfo__source',
    ).only(
        'slug',
        'buildinfo__sha1',
        'buildinfo__version',
        'buildinfo__source__name',
        'buildinfo__architecture__name',
        'key__name',
        'key__uid',
        'created',
    ).order_by()

    if 'key__uid' in request.GET:
        qs = qs.filter(key__uid__in=request.GET.getlist('key__uid'))

    grouped = groupby(
        sorted(qs, key=lambda x: (x.buildinfo.sha1, x.created)),
        lambda x: x.buildinfo.sha1,
        lambda x: x.created,
    )

    by_sha1 = [
        {
            'uri': '{}{}'.format(
                settings.SITE_URL,
                xs[0].get_absolute_url(),
            ),
            'sha1': sha1,
            'submissions': [{
                'key': {
                    'uid': x.key.uid,
                    'name': x.key.name,
                },
                'created': x.created,
            } for x in xs],
        }
        for sha1, xs in grouped
    ]

    return JsonResponse({'by_sha1': by_sha1})
