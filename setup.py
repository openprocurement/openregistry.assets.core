from setuptools import setup, find_packages

version = '0.1.1'

entry_points = {
    'openprocurement.api.plugins': [
        'assets.core = openregistry.assets.core.includeme:includeme'
    ],
    'openregistry.tests': [
        'assets.core = openregistry.assets.core.tests.main:suite'
    ]
}

test_requires = []

setup(name='openregistry.assets.core',
      version=version,
      description="",
      long_description=open("README.rst").read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='Quintagroup, Ltd.',
      author_email='info@quintagroup.com',
      license='Apache License 2.0',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['openregistry', 'openregistry.assets'],
      include_package_data=True,
      zip_safe=False,
      extras_require={'test': test_requires},
      entry_points=entry_points,
      )
