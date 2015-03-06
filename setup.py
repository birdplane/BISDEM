
from setuptools import setup, find_packages

kwargs = {'author': 'BirdPlane',
 'author_email': 'info@birdplane.nl',
 'classifiers': ['Intended Audience :: Science/Research',
                 'Topic :: Scientific/Engineering'],
 'description': '',
 'download_url': '',
 'include_package_data': True,
 'install_requires': ['openmdao.main'],
 'keywords': ['openmdao'],
 'license': '',
 'maintainer': '',
 'maintainer_email': '',
 'name': 'bisdem',
 'package_data': {'bisdem': []},
 'package_dir': {'': 'src'},
 'packages': ['bisdem'],
 'url': '',
 'version': '0.1',
 'zip_safe': False}


setup(**kwargs)

