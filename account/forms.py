from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from .models import User


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=100, help_text='Required. Add a valid email address')

	class Meta:
		model = User
		fields = ("email", "username", "password1", "password2")
		
	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs = {'class': 'login-input','placeholder': 'Email Address', 'autocapitalize':"off", 'autocorrect':"off", 'maxlength':"75"}
		self.fields['username'].widget.attrs = {'class': 'login-input','placeholder': 'Username', 'autocapitalize':"off", 'autocorrect':"off", 'maxlength':"75", 'minlength':"4"}
		self.fields['password1'].widget.attrs = {'class': 'login-input','placeholder': 'Password', 'autocapitalize':"off", 'autocorrect':"off"}
		self.fields['password2'].widget.attrs = {'class': 'login-input','placeholder': 'Password Confirmation', 'autocapitalize':"off", 'autocorrect':"off"}

class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
    	model = User
    	fields = ('email', 'password')

    def clean(self):
    	if self.is_valid():
    		email = self.cleaned_data['email']
    		password = self.cleaned_data['password']
    		if not authenticate(email=email, password=password):
                    raise forms.ValidationError("Invalid login")
        
    def __init__(self, *args, **kwargs):
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = {'placeholder': 'Email Address', 'class': 'login-input', 'autocapitalize':"off", 'autocorrect':"off", 'maxlength':"75"}
        self.fields['password'].widget.attrs = {'placeholder': 'Password', 'class': 'login-input', 'autocapitalize':"off", 'autocorrect':"off", 'maxlength':"75"}
        

class SettingsForm(forms.ModelForm):


    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'email',
            'bio',
            'website',
            'gender',
            'profile_pic',
        ]
    
    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'placeholder': 'Username', 'minlength':'4', 'class': 'input'}
        self.fields['name'].widget.attrs = {'placeholder': 'Name', 'class': 'input'}
        self.fields['email'].widget.attrs = {'placeholder': 'email', 'class': 'input'}
        self.fields['bio'].widget.attrs = {'placeholder': 'bio', 'class': 'input'}
        self.fields['website'].widget.attrs = {'placeholder': 'website', 'class': 'input'}
        self.fields['gender'].widget.attrs = {'placeholder': 'gender', 'class': 'input'}