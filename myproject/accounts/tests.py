from django.test import TestCase
from django.core.urlresolvers import reverse
from django.urls import resolve
from .views import signup
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Create your tests here.
class SignUpTests(TestCase):
	def test_signup_status_code(self):
		url =reverse('signup')
		response = self.client.get(url)
		self.assertEquals(response.status_code,200)
	def test_signup_url_resolves_signup_view(self):
		view = resolve('/signup/')
		self.assertEquals(view.func,signup)

class SuccessfulSignUpTests(TestCase):
	def setUp(self):
		url = reverse('signup')
		data = {
		   'username':'john',
		   'password1':'abcdef123456',
		    'password2':'abcdef123456'
        }
		self.response = self.client.post(url,data)
		self.home_url = reverse('home')

	def test_redirection(self):
		"""A valid form submission should redirect  the user to the homepage"""
		self.assertRedirects(self.response,self.home_url)

	def test_user_creation(self):
		self.assertTrue(User.objects.exists())

	def test_user_authentication(self):
		"""the resulting response should have a 'user' to its context after a successfull sign up"""
		response = self.client.get(self.home_url)
		user = response.context.get('user')
		self.assertFalse(user.is_authenticated)