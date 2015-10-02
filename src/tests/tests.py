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

    def test_divide(self):
        """
        Test a few instances of fields with a '/'.
        """
        form1 = TesterForm({'field1': '1/2', 'field2': '2/1', 'field3': '3/3'})
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form1.cleaned_data['field2'], Decimal('2'))
        self.assertEqual(form1.cleaned_data['field3'], Decimal('1'))

        form2 = TesterForm({'field1': '1/3', 'field2': '1/3', 'field3': '1/3'})
        self.assertTrue(form2.is_valid())
        self.assertEqual(form2.cleaned_data['field1'], Decimal('.33'))
        self.assertEqual(form2.cleaned_data['field2'], Decimal('.3'))
        self.assertEqual(form2.cleaned_data['field3'], Decimal('0'))

        form3 = TesterForm({'field1': '1/4', 'field2': '1/4', 'field3': '1/4'})
        self.assertTrue(form3.is_valid())
        self.assertEqual(form3.cleaned_data['field1'], Decimal('.25'))
        self.assertEqual(form3.cleaned_data['field2'], Decimal('.2'))
        self.assertEqual(form3.cleaned_data['field3'], Decimal('0'))

        form4 = TesterForm({'field1': '1/2', 'field2': '1/2', 'field3': '1/2'})
        self.assertTrue(form4.is_valid())
        self.assertEqual(form4.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field2'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field3'], Decimal('0'))

    def test_negative_numerators(self):
        """
        Test a few instances of negative numerators.
        """
        formN1 = TesterForm({'field1': '-1/2', 'field2': '-2/1', 'field3': '-3/3'})
        self.assertTrue(formN1.is_valid())
        self.assertEqual(formN1.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN1.cleaned_data['field2'], Decimal('-2'))
        self.assertEqual(formN1.cleaned_data['field3'], Decimal('-1'))

        formN2 = TesterForm({'field1': '-1/3', 'field2': '-1/3', 'field3': '-1/3'})
        self.assertTrue(formN2.is_valid())
        self.assertEqual(formN2.cleaned_data['field1'], Decimal('-.33'))
        self.assertEqual(formN2.cleaned_data['field2'], Decimal('-.3'))
        self.assertEqual(formN2.cleaned_data['field3'], Decimal('-0'))

        formN3 = TesterForm({'field1': '-1/4', 'field2': '-1/4', 'field3': '-1/4'})
        self.assertTrue(formN3.is_valid())
        self.assertEqual(formN3.cleaned_data['field1'], Decimal('-.25'))
        self.assertEqual(formN3.cleaned_data['field2'], Decimal('-.2'))
        self.assertEqual(formN3.cleaned_data['field3'], Decimal('0'))

        formN4 = TesterForm({'field1': '-1/2', 'field2': '-1/2', 'field3': '-1/2'})
        self.assertTrue(formN4.is_valid())
        self.assertEqual(formN4.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field2'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field3'], Decimal('0'))

    def test_negative_denominators(self):
        """
        Test a few instances of negative numerators.
        """
        formN1 = TesterForm({'field1': '1/-2', 'field2': '2/-1', 'field3': '3/-3'})
        self.assertTrue(formN1.is_valid())
        self.assertEqual(formN1.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN1.cleaned_data['field2'], Decimal('-2'))
        self.assertEqual(formN1.cleaned_data['field3'], Decimal('-1'))

        formN2 = TesterForm({'field1': '1/-3', 'field2': '1/-3', 'field3': '1/-3'})
        self.assertTrue(formN2.is_valid())
        self.assertEqual(formN2.cleaned_data['field1'], Decimal('-.33'))
        self.assertEqual(formN2.cleaned_data['field2'], Decimal('-.3'))
        self.assertEqual(formN2.cleaned_data['field3'], Decimal('-0'))

        formN3 = TesterForm({'field1': '1/-4', 'field2': '1/-4', 'field3': '1/-4'})
        self.assertTrue(formN3.is_valid())
        self.assertEqual(formN3.cleaned_data['field1'], Decimal('-.25'))
        self.assertEqual(formN3.cleaned_data['field2'], Decimal('-.2'))
        self.assertEqual(formN3.cleaned_data['field3'], Decimal('0'))

        formN4 = TesterForm({'field1': '1/-2', 'field2': '1/-2', 'field3': '1/-2'})
        self.assertTrue(formN4.is_valid())
        self.assertEqual(formN4.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field2'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field3'], Decimal('0'))

    def test_divide_negative_by_negative(self):
        """
        Ensure that -/- is positive.
        """
        form1 = TesterForm({'field1': '-1/-2', 'field2': '-2/-1', 'field3': '-3/-3'})
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form1.cleaned_data['field2'], Decimal('2'))
        self.assertEqual(form1.cleaned_data['field3'], Decimal('1'))

        form2 = TesterForm({'field1': '-1/-3', 'field2': '-1/-3', 'field3': '-1/-3'})
        self.assertTrue(form2.is_valid())
        self.assertEqual(form2.cleaned_data['field1'], Decimal('.33'))
        self.assertEqual(form2.cleaned_data['field2'], Decimal('.3'))
        self.assertEqual(form2.cleaned_data['field3'], Decimal('0'))

        form3 = TesterForm({'field1': '-1/-4', 'field2': '-1/-4', 'field3': '-1/-4'})
        self.assertTrue(form3.is_valid())
        self.assertEqual(form3.cleaned_data['field1'], Decimal('.25'))
        self.assertEqual(form3.cleaned_data['field2'], Decimal('.2'))
        self.assertEqual(form3.cleaned_data['field3'], Decimal('0'))

        form4 = TesterForm({'field1': '-1/-2', 'field2': '-1/-2', 'field3': '-1/-2'})
        self.assertTrue(form4.is_valid())
        self.assertEqual(form4.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field2'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field3'], Decimal('0'))

