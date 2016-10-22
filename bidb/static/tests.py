from bidb.utils.test import TestCase

class SmokeTest(TestCase):
    def setUp(self):
        super(SmokeTest, self).setUp()

    def test_landing(self):
        self.assertGET(200, 'static:landing')
