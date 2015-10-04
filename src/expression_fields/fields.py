from decimal import Decimal
from django.forms.fields import DecimalField
from django.forms.widgets import TextInput
from django.utils import formats
from django.utils.encoding import smart_text
from django.core.exceptions import ValidationError
from .expr import calculate


class DivideDecimalField(DecimalField):
    """A decimal field which allows the division operator."""
    widget = TextInput

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', "You can specify a decimal or use '/' to do simple division.")
        super(DivideDecimalField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if self.localize:
            value = formats.sanitize_separators(value)
        value = smart_text(value).strip()
        if '/' in value:
            numerator, denominator = value.split('/', 2)
            tp = super(DivideDecimalField, self).to_python
            value = tp(numerator) / tp(denominator)
            if value:
                # In Python 3, a simple round() call is enough. To support
                # Python 2, we have to do this quantize thing.
                quantize_target = ".".join(["1", "0" * self.decimal_places])
                return value.quantize(Decimal(quantize_target))
        else:
            return super(DivideDecimalField, self).to_python(value)


class DecimalExpressionField(DecimalField):
    """A decimal field which allows arbitrary math."""
    widget = TextInput

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('help_text', "You can specify a decimal or do simple arithmetic.")
        super(DecimalExpressionField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in self.empty_values:
            return None
        value = smart_text(value).strip()
        value = calculate(value)
        value = super(DecimalExpressionField, self).to_python(value)
        if value:
            # In Python 3, a simple round() call is enough. To support
            # Python 2, we have to do this quantize thing.
            try:
                quantize_target = ".".join(["1", "0" * self.decimal_places])
                return value.quantize(Decimal(quantize_target))
            except (ValueError, TypeError):
                raise ValidationError('Enter an expression.', code='invalid')


class FutureField(object):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError


class FloatExpressionField(FutureField):
    pass


class IntegerExpressionField(FutureField):
    pass
