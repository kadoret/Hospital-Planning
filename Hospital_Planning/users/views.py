#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from users.models import Users

def index(request):
	anUserList = Users.objects.all()
	return render(request, 'users/index.html', {'userList': anUserList})
