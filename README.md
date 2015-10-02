Introduction
------------

django-expression-fields lets your users type a mathematical expression in a form field.
Python does the math and stores the result in the database. For example, suppose you have a model to track Things, like this:

    class Thing(models.Model):
    	cost = models.DecimalField(
    		max_digits=5, decimal_places=2, null=True, blank=True)

Suppose Things come in packs of 12 for $7.99. Your users have to do some math to fill in the cost of a single Thing, $0.67.

But not with an expression field! Create your form like this:

	class ThingForm(forms.Form):
		cost = DecimalExpressionField(
			max_digits=5, decimal_places=2, required=False)

Now your user can simply type `7.99/12` in the field and Python will do the math for them!


Requirements and Installation
-----------------------------

Right now, the project has no dependencies.

* `pip install django-expression-fields`
* Add expression_fields to your INSTALLED_APPS.


Use
---

	from django import forms
	from expression_fields.fields import DivideDecimalField

	class MyForm(forms.Form):
		cost = DecimalExpressionField(
			max_digits=5, decimal_places=2, required=False)


Tests
-----

`./run-tests.sh`.


Limitations
-----------

* Only `DecimalExpressionField` exists today. I later intend to build Integer and Float expression fields as well.
* This field slightly changes the behavior of the existing `DecimalField`: Inputs that would rejected for having too many digits after the decimal are instead rounded.
* For historical reasons, there's a `DivideDecimalField` which allows a single division sign.


Contributions
-------------

I built this little project to satisfy a personal need, but thought it might be useful enough for others.
If you have contributions, please don't hesitate to send a PR.
Let's keep the tests passing and all will be well.
My personal stack is currently Django 1.8 on Python 3.4, but once I can get some Travis set up, there's no reason not to support other versions.
