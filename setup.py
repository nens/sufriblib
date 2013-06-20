from setuptools import setup

version = '0.4.dev0'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'setuptools',
    'pyproj',
    ],

tests_require = [
    'nose',
    'coverage',
    ]

setup(name='sufriblib',
      version=version,
      description="A library for working with SUFRIB 2.1 files (.RIB and .RMB files, sewer system measurement data)",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[],
      keywords=[],
      author='Remco Gerlich',
      author_email='remco.gerlich@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['sufriblib'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
            'sufribcat=sufriblib.scripts:sufribcat',
          ]},
      )
