from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.template.defaultfilters import slugify
from django.contrib import messages

from .forms import RegistrationForm, AccountAuthenticationForm, SettingsForm
from .models import User
from .decorators import unauthorizedUserCanView, authorizedUserCanView

@unauthorizedUserCanView
def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)

			obj.username = slugify(obj.username)
			
			obj.save() 
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('/')
		else:
			context['form'] = form
	else:
		form = RegistrationForm()
		context['form'] = form
	return render(request, 'account/register.html', context)

@unauthorizedUserCanView
def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated:
		return redirect("/")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("/")
		else:
			messages.error(request, "Invalid login. Note: Email field is case-sensitive")

	else:
		form = AccountAuthenticationForm()

	context['form'] = form
	return render(request, 'account/login.html', context)

@authorizedUserCanView
def logout_view(request):
	logout(request)
	return redirect('/')

@authorizedUserCanView
def settings_view(request):
	myinstance = User.objects.filter(username=request.user).first()
	form = SettingsForm(instance=myinstance)

	if request.method == 'POST':
		form = SettingsForm(request.POST, request.FILES, instance=myinstance)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.username = slugify(obj.username)
			obj.save()

			messages.success(request, 'Profile Saved.')
			return redirect('/')
		else:
			messages.error(request, 'Can\' save changes.')
	else:
		myinstance = User.objects.filter(username=request.user).first()
		form = SettingsForm(instance=myinstance)

	context = {'form': form}
	search = request.GET.get('search')
	if search:
		results = User.objects.filter(username__icontains=search)
		context['results'] = results
	else:
		User.objects.all()
		search = ''
	return render(request, 'account/settings.html', context)