from django.shortcuts import render, get_object_or_404

from .models import Binary, Source

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
