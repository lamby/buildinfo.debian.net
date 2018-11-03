import datetime
import time

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import SuspiciousOperation

from ..buildinfo.models import Buildinfo

from .utils import parse_submission, InvalidSubmission


@csrf_exempt
@require_http_methods(['PUT'])
def submit(request):
    try:
        submission, created = parse_submission(request)
    except InvalidSubmission as exc:
        return HttpResponseBadRequest("Rejecting submission: {}\n".format(exc))

    return HttpResponse('{}{}\n'.format(
        settings.SITE_URL,
        submission.buildinfo.get_absolute_url(),
    ), status=201 if created else 200)


@require_http_methods(['GET'])
def buildinfo_since(request, date):
    try:
        created = datetime.datetime.fromtimestamp(int(date) + 1)
    except ValueError:
        raise HttpResponseBadRequest("Date value should be an integer")
    try:
        limit = int(request.GET.get('limit', 100))
        if limit <= 0:
            raise HttpResponseBadRequest("Limit value should be positive")
    except ValueError:
        raise HttpResponseBadRequest("Limit value should be an integer")

    buildinfo = Buildinfo.objects.filter(
            created__gte=created,
    ).select_related(
        'source',
        'architecture',
    ).order_by('created')[:limit]

    return JsonResponse({'buildinfos': [{
        'uri': '{}{}'.format(
            settings.SITE_URL,
            x.get_absolute_url(),
        ),
        'raw-uri': '{}{}'.format(
            settings.SITE_URL,
            x.get_absolute_raw_url(),
        ),
        'source': x.source.name,
        'version': x.version,
        'architecture': x.architecture.name,
        'created':  time.mktime(x.created.timetuple()),
    } for x in buildinfo]})
