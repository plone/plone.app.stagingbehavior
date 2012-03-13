from setuptools import setup, find_packages
import os

version = '0.1b4'

setup(name='plone.app.stagingbehavior',
      version=version,
      description="Provides a behavior for using plone.app.iterate with dexterity content types",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone dexterity behavior iterate staging',
      author='Jonas Baumann',
      author_email='dexterity-development@googlegroups.com',
      url='http://plone.org/products/dexterity',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone',
          'plone.app.dexterity',
          'plone.app.iterate',
          'plone.app.relationfield',
          'plone.locking',
          'z3c.relationfield',
          # -*- Extra requirements: -*-
      ],
      extras_require = {
        'test':  [
            'plone.app.testing',
            'plone.app.versioningbehavior',
            'plone.app.referenceablebehavior',
            'Products.CMFPlacefulWorkflow',
            ],
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
