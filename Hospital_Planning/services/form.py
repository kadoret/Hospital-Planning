from django import forms
from django.contrib.auth import login, authenticate
from services.models import doctors

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30)
	password = forms.CharField(max_length=30)

	def is_valid(self, *args, **kwargs):
		request = kwargs.pop('request')
		super(LoginForm, self).is_valid(*args, **kwargs)
		user = authenticate(username= self.cleaned_data['username'], 
					password=self.cleaned_data['password'] )
		if user is not None:
 			if user.is_active:
 				login(request, user)
				return True
		return False
		
