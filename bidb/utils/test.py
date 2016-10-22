from django.test import TestCase
from django.shortcuts import resolve_url

class TestCase(TestCase):
    def assertStatusCode(self, status_code, fn, urlconf, *args, **kwargs):
        response = fn(resolve_url(urlconf, *args, **kwargs))

        self.assertEqual(
            response.status_code,
            status_code,
            "Got HTTP %d but expected HTTP %d. Response:\n%s" % (
                response.status_code,
                status_code,
                response,
            )
        )

        return response

    def assertGET(self, status_code, urlconf, *args, **kwargs):
        return self.assertStatusCode(
            status_code,
            self.client.get,
            urlconf,
            *args,
            **kwargs
        )

    def assertPOST(self, status_code, data, *args, **kwargs):
        return self.assertStatusCode(
            status_code, lambda x: self.client.post(x, data), *args, **kwargs
        )

    def assertRedirectsTo(self, response, urlconf, *args, **kwargs):
        status_code = kwargs.pop('status_code', 302)
        target_status_code = kwargs.pop('target_status_code', 200)

        return self.assertRedirects(
            response,
            resolve_url(urlconf, *args, **kwargs),
            status_code,
            target_status_code,
        )
