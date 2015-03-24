from django.shortcuts import render_to_response
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from authentication.models import *


def login_user(request):
	logout(request)
	username = password = ''
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username = username, password = password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/main')
	return render_to_response('login/login.html', context_instance=RequestContext(request))


@login_required(login_url='/login/')
def main(request):
	return redirect('authenticate.views.main')
