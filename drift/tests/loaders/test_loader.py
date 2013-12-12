from django.utils.unittest import TestCase
from drift.tests.mocks import fixtures
from drift.loaders import Loader


class LoaderTestCase(TestCase):
    def setUp(self):
        self.loader = Loader(fixtures['excel'], autoload=False)

    def test_close_raises_not_implemented(self):
        def loader_open(): self.loader.open()
        self.assertRaises(NotImplementedError, loader_open)

    def test_sniff(self):
        for name in fixtures:
            self.assertEqual(Loader.sniff(fixtures[name]), False)
