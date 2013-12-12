import drift.tests
import os


drift_tests_path = os.path.dirname(drift.tests.__file__)


def is_dotfile(path): return os.path.basename(path)[0] == '.'
def not_dotfile(path): return not is_dotfile(path)


class Fixture:
    root = os.path.join(drift_tests_path, 'fixtures')

    def __init__(self, path='excel.xlsx'):
        self.path = self.full_path(path)
        self.data = open(self.path, 'r').read()

    @classmethod
    def full_path(cls, path):
        return os.path.join(cls.root, path)


fixture_names = filter(not_dotfile, os.listdir(Fixture.root))


def get_fixture_mapping(name):
    name_without_extension = '.'.join(name.split('.')[:-1])

    return (
        name_without_extension,
        Fixture(name)
    )


fixtures = dict(map(get_fixture_mapping, fixture_names))
