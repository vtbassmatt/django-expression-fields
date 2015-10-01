from django.forms.fields import DecimalField
from django.forms.widgets import TextInput
from django.utils import formats
from django.utils.encoding import smart_text


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
            numerator, denominator = value.split('/', maxsplit=2)
            tp = super(DivideDecimalField, self).to_python
            return round(tp(numerator) / tp(denominator), self.decimal_places)
        else:
            return super(DivideDecimalField, self).to_python(value)
