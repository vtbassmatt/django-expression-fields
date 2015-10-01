import os
from setuptools import setup, find_packages

version = '0.1.1'

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-expression-fields',
    version = version,
    description = 'django-expression-fields allows typing mathematical expressions into form fields and having only the calculated result stored in the database.',
    keywords = 'django field expression math',
    license = 'MIT License',
    author = 'Matt Cooper',
    author_email = 'vtbassmatt@gmail.com',
    url = 'http://github.com/vtbassmatt/django-expression-fields/',
    install_requires = [],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    package_dir = {'': 'src'},
    packages = ['expression_fields'],
    include_package_data = True,
)

