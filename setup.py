from setuptools import setup, find_packages
import sys, os

version = '0.0'

requires = [
    'SQLAlchemy',
    'feedparser',      # only needed for rss collection
    'psycopg2',        # dbapi for postgresql
    'robobrowser',
    'beautifulsoup4',
    'transaction',     # I am not sure if I should use this or not
    'PyPDF2',           # processing of legistar pdf's
    'zope.sqlalchemy',
    'requests',
    'cornice',
    ]


setup(name='hubby',
      version=version,
      setup_requires=[],
      description="track and analyze municipal legislation",
      long_description="""\
track and analyze municipal legislation""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Joseph Rawson',
      author_email='joseph.rawson.works@gmail.com',
      url='https://github.com/umeboshi2/hubby',
      license='Public Domain',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      #test_suite='hubby',
      install_requires=requires,
      entry_points="""\
      # -*- Entry points: -*-
      [paste.app_factory]
      main = hubby:main
      [console_scripts]
      initialize_hubby_db = hubby.scripts.initializedb:main
      """,
      dependency_links=[
        'https://github.com/knowah/PyPDF2/archive/master.tar.gz#egg=PyPDF2-1.15dev',
        ]
      )


