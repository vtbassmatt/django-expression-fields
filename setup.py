import os
from setuptools import setup, find_packages

version = '0.2.0'
README = """
django-expression-fields lets your users type a mathematical expression in a form field.
Python does the math and stores the result in the database. For example, suppose you have a model to track Things, like this::

    class Thing(models.Model):
    	cost = models.DecimalField(
    		max_digits=5, decimal_places=2, null=True, blank=True)

Suppose Things come in packs of 12 for $7.99. Your users have to do some math to fill in the cost of a single Thing, $0.67.

But not with an expression field! Create your form like this::

	class ThingForm(forms.Form):
		cost = DecimalExpressionField(
			max_digits=5, decimal_places=2, required=False)

Now your user can simply type ``7.99/12`` in the field and Python will do the math for them!
"""

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-expression-fields',
    version = version,
    description = 'django-expression-fields allows typing mathematical expressions into form fields and having only the calculated result stored in the database.',
    long_description = README,
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

