import unittest
from decimal import Decimal
from django.forms import Form
from expression_fields.fields import DivideDecimalField


class TesterForm(Form):
    field1 = DivideDecimalField(max_digits=5, decimal_places=2, required=False)
    field2 = DivideDecimalField(max_digits=4, decimal_places=1)
    field3 = DivideDecimalField(max_digits=5, decimal_places=0, required=False)


class DivideDecimalTests(unittest.TestCase):

    def test_base_behavior(self):
        """
        Sanity test to make sure we didn't break the base DecimalField.
        """
        form1 = TesterForm({'field1': '256.32', 'field2': '123.4'})
        form2 = TesterForm({'field1': '256', 'field2': '123'})
        form3 = TesterForm({'field2': '123'})
        form4 = TesterForm({'field1': '123'})
        form5 = TesterForm({'field2': '123', 'field3': '456'})
        form6 = TesterForm({'field2': '123', 'field3': '456.0'})
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['field1'], Decimal('256.32'))
        self.assertEqual(form1.cleaned_data['field2'], Decimal('123.4'))
        self.assertTrue(form2.is_valid())
        self.assertEqual(form2.cleaned_data['field1'], Decimal('256'))
        self.assertEqual(form2.cleaned_data['field2'], Decimal('123'))
        self.assertTrue(form3.is_valid())
        self.assertFalse(form4.is_valid())
        self.assertTrue(form5.is_valid())
        self.assertFalse(form6.is_valid())
