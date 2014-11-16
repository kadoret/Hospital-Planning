from django import forms
from django.contrib.auth import login, authenticate
from services.models import doctors, jobs
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


class LoginForm(AuthenticationForm):
	
	def is_valid(self, *args, **kwargs):
		request = kwargs.pop('request')
		super(LoginForm, self).is_valid(*args, **kwargs)
		if 'old_password' in request.POST:
			user = authenticate(username= request.user,
						password=request.POST['old_password'] )
		else:
			user = authenticate(username= self.request['username'], 
					password=self.request['password'] )
		if user is not None:
 			if user.is_active:
 				login(request, user)
				return True
		return False

class doctorForm(UserCreationForm):
	username = forms.RegexField(label=("Identifiant"), max_length=30, regex=r'^[ \t\r\n\f\w.@+*-]+$',
	help_text = ("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
	error_messages = {'invalid': ("This value may contain only letters, numbers and @/./+/-/_ characters.")})
	email = forms.CharField(max_length=75, required=True)
	class Meta:
		model = doctors

class doctorChangeForm(UserChangeForm):
	username = forms.RegexField(label=("Identifiant"), max_length=30, regex=r'^[ \t\r\n\f\w.@+*-]+$',
	help_text = ("Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."),
	error_messages = {'invalid': ("This value may contain only letters, numbers and @/./+/-/_ characters.")})
	email = forms.CharField(max_length=75, required=True)
	class Meta:
		model = doctors
