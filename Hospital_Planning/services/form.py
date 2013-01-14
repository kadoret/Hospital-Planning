from django import forms
from django.contrib.auth import login, authenticate
from services.models import doctors
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
	
	def is_valid(self, *args, **kwargs):
		request = kwargs.pop('request')
		super(LoginForm, self).is_valid(*args, **kwargs)
		user = authenticate(username= self.request['username'], 
					password=self.request['password'] )
		if user is not None:
 			if user.is_active:
 				login(request, user)
				return True
		return False
