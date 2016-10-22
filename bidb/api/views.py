from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .utils import parse_submission, InvalidSubmission


@csrf_exempt
@require_http_methods(['PUT'])
def submit(request):
    try:
        submission, created = parse_submission(request)
    except InvalidSubmission as exc:
        return HttpResponseBadRequest("{}\n".format(exc))

    return HttpResponse('{}{}\n'.format(
        settings.SITE_URL,
        submission.buildinfo.get_absolute_url(),
    ), status=201 if created else 200)
