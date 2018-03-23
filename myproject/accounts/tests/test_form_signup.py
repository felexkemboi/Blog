from django.test import TestCase
from ..forms import SignUpForm

def SignUpTest(TestCase):
	def test_form_has_fields(self):
		form = SignUpForm()
		expected = ['username','email','password1','password2']
		actual = list(form.fields)
		self.assertSequence(expected,actual)