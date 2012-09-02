from distutils.core import setup

import os
import sys

parent_directory = os.path.abspath(os.path.dirname(__file__))

metafiles = {
    'README.md': None,
    'CHANGES.md': None,
    'CLASSIFIERS.txt': None,
}

# The following bit will read each index from metafiles and fill it's value
# with the contents of that file if it is able to read the file.
for filename in metafiles:
    try:
        current_file = open(os.path.join(parent_directory, filename))
        metafiles[filename] = current_file.read()
        current_file.close()

    except IOError:
        pass

# No dependencies :)
dependencies = []

metadata = {
    'name': 'django-importer-better',
    'version': '0.1',
    'description': 'Takes files and turns them into recrods in models. HOORAY!',
    'long_description': metafiles['README.md'] + '\n\n' + metafiles['CHANGES.md'],
    'classifiers': metafiles['CLASSIFIERS.txt'],
    'author': 'Brandon R. Stoner',
    'author_email': 'monokrome@limpidtech.com',
    'url': 'http://github.com/monokrome/django-importer',
    'keywords': '',
    'packages': ['importer'],
    'install_requires': dependencies,
    'tests_require': dependencies,
}

setup(**metadata)

