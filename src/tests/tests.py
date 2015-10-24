import unittest
from decimal import Decimal
from django.forms import Form
from expression_fields.fields import DivideDecimalField, DecimalExpressionField


class DivDecForm(Form):
    field1 = DivideDecimalField(max_digits=5, decimal_places=2, required=False)
    field2 = DivideDecimalField(max_digits=4, decimal_places=1)
    field3 = DivideDecimalField(max_digits=5, decimal_places=0, required=False)


class DivideDecimalTests(unittest.TestCase):

    def test_base_behavior(self):
        """
        Sanity test to make sure we didn't break the base DecimalField.
        """
        form1 = DivDecForm({'field1': '256.32', 'field2': '123.4'})
        form2 = DivDecForm({'field1': '256', 'field2': '123'})
        form3 = DivDecForm({'field2': '123'})
        form4 = DivDecForm({'field1': '123'})
        form5 = DivDecForm({'field2': '123', 'field3': '456'})
        form6 = DivDecForm({'field2': '123', 'field3': '456.0'})
        form7 = DivDecForm({'field1': '', 'field2': '0.0'})
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
        self.assertTrue(form7.is_valid())
        self.assertEqual(form7.cleaned_data['field1'], None)
        self.assertEqual(form7.cleaned_data['field2'], Decimal('0'))
        self.assertEqual(form7.cleaned_data['field3'], None)

    def test_divide(self):
        """
        Test a few instances of fields with a '/'.
        """
        form1 = DivDecForm({'field1': '1/2', 'field2': '2/1', 'field3': '3/3'})
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form1.cleaned_data['field2'], Decimal('2'))
        self.assertEqual(form1.cleaned_data['field3'], Decimal('1'))

        form2 = DivDecForm({'field1': '1/3', 'field2': '1/3', 'field3': '1/3'})
        self.assertTrue(form2.is_valid())
        self.assertEqual(form2.cleaned_data['field1'], Decimal('.33'))
        self.assertEqual(form2.cleaned_data['field2'], Decimal('.3'))
        self.assertEqual(form2.cleaned_data['field3'], Decimal('0'))

        form3 = DivDecForm({'field1': '1/4', 'field2': '1/4', 'field3': '1/4'})
        self.assertTrue(form3.is_valid())
        self.assertEqual(form3.cleaned_data['field1'], Decimal('.25'))
        self.assertEqual(form3.cleaned_data['field2'], Decimal('.2'))
        self.assertEqual(form3.cleaned_data['field3'], Decimal('0'))

        form4 = DivDecForm({'field1': '1/2', 'field2': '1/2', 'field3': '1/2'})
        self.assertTrue(form4.is_valid())
        self.assertEqual(form4.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field2'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field3'], Decimal('0'))

    def test_negative_numerators(self):
        """
        Test a few instances of negative numerators.
        """
        formN1 = DivDecForm({'field1': '-1/2', 'field2': '-2/1', 'field3': '-3/3'})
        self.assertTrue(formN1.is_valid())
        self.assertEqual(formN1.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN1.cleaned_data['field2'], Decimal('-2'))
        self.assertEqual(formN1.cleaned_data['field3'], Decimal('-1'))

        formN2 = DivDecForm({'field1': '-1/3', 'field2': '-1/3', 'field3': '-1/3'})
        self.assertTrue(formN2.is_valid())
        self.assertEqual(formN2.cleaned_data['field1'], Decimal('-.33'))
        self.assertEqual(formN2.cleaned_data['field2'], Decimal('-.3'))
        self.assertEqual(formN2.cleaned_data['field3'], Decimal('-0'))

        formN3 = DivDecForm({'field1': '-1/4', 'field2': '-1/4', 'field3': '-1/4'})
        self.assertTrue(formN3.is_valid())
        self.assertEqual(formN3.cleaned_data['field1'], Decimal('-.25'))
        self.assertEqual(formN3.cleaned_data['field2'], Decimal('-.2'))
        self.assertEqual(formN3.cleaned_data['field3'], Decimal('0'))

        formN4 = DivDecForm({'field1': '-1/2', 'field2': '-1/2', 'field3': '-1/2'})
        self.assertTrue(formN4.is_valid())
        self.assertEqual(formN4.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field2'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field3'], Decimal('0'))

    def test_negative_denominators(self):
        """
        Test a few instances of negative numerators.
        """
        formN1 = DivDecForm({'field1': '1/-2', 'field2': '2/-1', 'field3': '3/-3'})
        self.assertTrue(formN1.is_valid())
        self.assertEqual(formN1.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN1.cleaned_data['field2'], Decimal('-2'))
        self.assertEqual(formN1.cleaned_data['field3'], Decimal('-1'))

        formN2 = DivDecForm({'field1': '1/-3', 'field2': '1/-3', 'field3': '1/-3'})
        self.assertTrue(formN2.is_valid())
        self.assertEqual(formN2.cleaned_data['field1'], Decimal('-.33'))
        self.assertEqual(formN2.cleaned_data['field2'], Decimal('-.3'))
        self.assertEqual(formN2.cleaned_data['field3'], Decimal('-0'))

        formN3 = DivDecForm({'field1': '1/-4', 'field2': '1/-4', 'field3': '1/-4'})
        self.assertTrue(formN3.is_valid())
        self.assertEqual(formN3.cleaned_data['field1'], Decimal('-.25'))
        self.assertEqual(formN3.cleaned_data['field2'], Decimal('-.2'))
        self.assertEqual(formN3.cleaned_data['field3'], Decimal('0'))

        formN4 = DivDecForm({'field1': '1/-2', 'field2': '1/-2', 'field3': '1/-2'})
        self.assertTrue(formN4.is_valid())
        self.assertEqual(formN4.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field2'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field3'], Decimal('0'))

    def test_divide_negative_by_negative(self):
        """
        Ensure that -/- is positive.
        """
        form1 = DivDecForm({'field1': '-1/-2', 'field2': '-2/-1', 'field3': '-3/-3'})
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form1.cleaned_data['field2'], Decimal('2'))
        self.assertEqual(form1.cleaned_data['field3'], Decimal('1'))

        form2 = DivDecForm({'field1': '-1/-3', 'field2': '-1/-3', 'field3': '-1/-3'})
        self.assertTrue(form2.is_valid())
        self.assertEqual(form2.cleaned_data['field1'], Decimal('.33'))
        self.assertEqual(form2.cleaned_data['field2'], Decimal('.3'))
        self.assertEqual(form2.cleaned_data['field3'], Decimal('0'))

        form3 = DivDecForm({'field1': '-1/-4', 'field2': '-1/-4', 'field3': '-1/-4'})
        self.assertTrue(form3.is_valid())
        self.assertEqual(form3.cleaned_data['field1'], Decimal('.25'))
        self.assertEqual(form3.cleaned_data['field2'], Decimal('.2'))
        self.assertEqual(form3.cleaned_data['field3'], Decimal('0'))

        form4 = DivDecForm({'field1': '-1/-2', 'field2': '-1/-2', 'field3': '-1/-2'})
        self.assertTrue(form4.is_valid())
        self.assertEqual(form4.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field2'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field3'], Decimal('0'))


class DecExprForm(Form):
    field1 = DecimalExpressionField(max_digits=5, decimal_places=2, required=False)
    field2 = DecimalExpressionField(max_digits=4, decimal_places=1)
    field3 = DecimalExpressionField(max_digits=5, decimal_places=0, required=False)


class DecimalExpressionDivisionTests(unittest.TestCase):
    """Cloned from DivideDecimalField tests"""
    def test_base_behavior(self):
        """
        Sanity test to make sure we didn't break the base DecimalField.
        """
        form1 = DecExprForm({'field1': '256.32', 'field2': '123.4'})
        form2 = DecExprForm({'field1': '256', 'field2': '123'})
        form3 = DecExprForm({'field2': '123'})
        form4 = DecExprForm({'field1': '123'})
        form5 = DecExprForm({'field2': '123', 'field3': '456'})
        form6 = DecExprForm({'field2': '123', 'field3': '456.0'})
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['field1'], Decimal('256.32'))
        self.assertEqual(form1.cleaned_data['field2'], Decimal('123.4'))
        self.assertTrue(form2.is_valid())
        self.assertEqual(form2.cleaned_data['field1'], Decimal('256'))
        self.assertEqual(form2.cleaned_data['field2'], Decimal('123'))
        self.assertTrue(form3.is_valid())
        self.assertFalse(form4.is_valid())
        self.assertTrue(form5.is_valid())
        # The assertion below would fail since all inputs are rounded
        # to the correct number of digits after the decimal. This is
        # documented in the README.
        # self.assertFalse(form6.is_valid())

    def test_divide(self):
        """
        Test a few instances of fields with a '/'.
        """
        form1 = DecExprForm({'field1': '1/2', 'field2': '2/1', 'field3': '3/3'})
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form1.cleaned_data['field2'], Decimal('2'))
        self.assertEqual(form1.cleaned_data['field3'], Decimal('1'))

        form2 = DecExprForm({'field1': '1/3', 'field2': '1/3', 'field3': '1/3'})
        self.assertTrue(form2.is_valid())
        self.assertEqual(form2.cleaned_data['field1'], Decimal('.33'))
        self.assertEqual(form2.cleaned_data['field2'], Decimal('.3'))
        self.assertEqual(form2.cleaned_data['field3'], Decimal('0'))

        form3 = DecExprForm({'field1': '1/4', 'field2': '1/4', 'field3': '1/4'})
        self.assertTrue(form3.is_valid())
        self.assertEqual(form3.cleaned_data['field1'], Decimal('.25'))
        self.assertEqual(form3.cleaned_data['field2'], Decimal('.2'))
        self.assertEqual(form3.cleaned_data['field3'], Decimal('0'))

        form4 = DecExprForm({'field1': '1/2', 'field2': '1/2', 'field3': '1/2'})
        self.assertTrue(form4.is_valid())
        self.assertEqual(form4.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field2'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field3'], Decimal('0'))

    def test_negative_numerators(self):
        """
        Test a few instances of negative numerators.
        """
        formN1 = DecExprForm({'field1': '-1/2', 'field2': '-2/1', 'field3': '-3/3'})
        self.assertTrue(formN1.is_valid())
        self.assertEqual(formN1.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN1.cleaned_data['field2'], Decimal('-2'))
        self.assertEqual(formN1.cleaned_data['field3'], Decimal('-1'))

        formN2 = DecExprForm({'field1': '-1/3', 'field2': '-1/3', 'field3': '-1/3'})
        self.assertTrue(formN2.is_valid())
        self.assertEqual(formN2.cleaned_data['field1'], Decimal('-.33'))
        self.assertEqual(formN2.cleaned_data['field2'], Decimal('-.3'))
        self.assertEqual(formN2.cleaned_data['field3'], Decimal('-0'))

        formN3 = DecExprForm({'field1': '-1/4', 'field2': '-1/4', 'field3': '-1/4'})
        self.assertTrue(formN3.is_valid())
        self.assertEqual(formN3.cleaned_data['field1'], Decimal('-.25'))
        self.assertEqual(formN3.cleaned_data['field2'], Decimal('-.2'))
        self.assertEqual(formN3.cleaned_data['field3'], Decimal('0'))

        formN4 = DecExprForm({'field1': '-1/2', 'field2': '-1/2', 'field3': '-1/2'})
        self.assertTrue(formN4.is_valid())
        self.assertEqual(formN4.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field2'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field3'], Decimal('0'))

    def test_negative_denominators(self):
        """
        Test a few instances of negative numerators.
        """
        formN1 = DecExprForm({'field1': '1/-2', 'field2': '2/-1', 'field3': '3/-3'})
        self.assertTrue(formN1.is_valid())
        self.assertEqual(formN1.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN1.cleaned_data['field2'], Decimal('-2'))
        self.assertEqual(formN1.cleaned_data['field3'], Decimal('-1'))

        formN2 = DecExprForm({'field1': '1/-3', 'field2': '1/-3', 'field3': '1/-3'})
        self.assertTrue(formN2.is_valid())
        self.assertEqual(formN2.cleaned_data['field1'], Decimal('-.33'))
        self.assertEqual(formN2.cleaned_data['field2'], Decimal('-.3'))
        self.assertEqual(formN2.cleaned_data['field3'], Decimal('-0'))

        formN3 = DecExprForm({'field1': '1/-4', 'field2': '1/-4', 'field3': '1/-4'})
        self.assertTrue(formN3.is_valid())
        self.assertEqual(formN3.cleaned_data['field1'], Decimal('-.25'))
        self.assertEqual(formN3.cleaned_data['field2'], Decimal('-.2'))
        self.assertEqual(formN3.cleaned_data['field3'], Decimal('0'))

        formN4 = DecExprForm({'field1': '1/-2', 'field2': '1/-2', 'field3': '1/-2'})
        self.assertTrue(formN4.is_valid())
        self.assertEqual(formN4.cleaned_data['field1'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field2'], Decimal('-.5'))
        self.assertEqual(formN4.cleaned_data['field3'], Decimal('0'))

    def test_divide_negative_by_negative(self):
        """
        Ensure that -/- is positive.
        """
        form1 = DecExprForm({'field1': '-1/-2', 'field2': '-2/-1', 'field3': '-3/-3'})
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form1.cleaned_data['field2'], Decimal('2'))
        self.assertEqual(form1.cleaned_data['field3'], Decimal('1'))

        form2 = DecExprForm({'field1': '-1/-3', 'field2': '-1/-3', 'field3': '-1/-3'})
        self.assertTrue(form2.is_valid())
        self.assertEqual(form2.cleaned_data['field1'], Decimal('.33'))
        self.assertEqual(form2.cleaned_data['field2'], Decimal('.3'))
        self.assertEqual(form2.cleaned_data['field3'], Decimal('0'))

        form3 = DecExprForm({'field1': '-1/-4', 'field2': '-1/-4', 'field3': '-1/-4'})
        self.assertTrue(form3.is_valid())
        self.assertEqual(form3.cleaned_data['field1'], Decimal('.25'))
        self.assertEqual(form3.cleaned_data['field2'], Decimal('.2'))
        self.assertEqual(form3.cleaned_data['field3'], Decimal('0'))

        form4 = DecExprForm({'field1': '-1/-2', 'field2': '-1/-2', 'field3': '-1/-2'})
        self.assertTrue(form4.is_valid())
        self.assertEqual(form4.cleaned_data['field1'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field2'], Decimal('.5'))
        self.assertEqual(form4.cleaned_data['field3'], Decimal('0'))


class DecimalExpressionTests(unittest.TestCase):
    """more interesting expressions to test"""
    def test_valid(self):
        """
        Some simple valid expressions.
        """
        form1 = DecExprForm({'field1': '-2+1', 'field2': '1-2', 'field3': '1+-2'})
        self.assertTrue(form1.is_valid())
        self.assertEqual(form1.cleaned_data['field1'], Decimal('-1'))
        self.assertEqual(form1.cleaned_data['field2'], Decimal('-1'))
        self.assertEqual(form1.cleaned_data['field3'], Decimal('-1'))

        form2 = DecExprForm({'field1': 'pi', 'field2': 'pi', 'field3': 'pi'})
        self.assertTrue(form2.is_valid())
        self.assertEqual(form2.cleaned_data['field1'], Decimal('3.14'))
        self.assertEqual(form2.cleaned_data['field2'], Decimal('3.1'))
        self.assertEqual(form2.cleaned_data['field3'], Decimal('3'))

        form3 = DecExprForm({'field1': 'sin(90)', 'field2': 'cos(-180)*100', 'field3': 'pow(2,5)'})
        self.assertTrue(form3.is_valid())
        self.assertEqual(form3.cleaned_data['field1'], Decimal('0.89'))
        self.assertEqual(form3.cleaned_data['field2'], Decimal('-59.8'))
        self.assertEqual(form3.cleaned_data['field3'], Decimal('32'))

        form4 = DecExprForm({'field1': 'abs(-1/2)', 'field2': 'abs(-10)', 'field3': 'sqrt(4)'})
        self.assertTrue(form4.is_valid())
        self.assertEqual(form4.cleaned_data['field1'], Decimal('0.5'))
        self.assertEqual(form4.cleaned_data['field2'], Decimal('10'))
        self.assertEqual(form4.cleaned_data['field3'], Decimal('2'))

    def test_invalid(self):
        """
        Some ways to try and blow it up.
        """
        formN1 = DecExprForm({'field1': 'ceil', 'field2': 'int', 'field3': '2+x'})
        self.assertFalse(formN1.is_valid())

        formN2 = DecExprForm({'field1': '-', 'field2': '*', 'field3': '2++3'})
        self.assertFalse(formN2.is_valid())

        formN3 = DecExprForm({'field1': '1**2', 'field2': 'pow(1,2,3)', 'field3': 'abs(5,6)'})
        self.assertFalse(formN3.is_valid())
