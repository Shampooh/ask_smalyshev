# -*- coding: utf-8 -*-

#middleware!!!!!!!!!!!
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pformat
from cgi import parse_qsl, escape
from loremipsum import get_sentence
from loremipsum import get_paragraph
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from MalyshevAsk.models import User, Question, Answer, Like, Tag, UserManager, QuestionManager, AnswerManager
from MalyshevAsk.forms import RegistrationForm,  ProfileForm, LoginForm, New_question_Form, New_answer_form
import random 
import re
from MalyshevAsk.models import User
from django.contrib.auth import login as authorization	
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.template import RequestContext
from django.contrib.auth import logout as deAuthorization
import datetime
import requests
# Create your views here.

def paginate(objects_list, request):
	paginator = Paginator(objects_list, 5)
	page = request.GET.get('page')
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		questions = paginator.page(1)
	except EmptyPage:
		questions = paginator.page(paginator.num_pages)
	return questions

def index(request):
	objects_list = Question.objects.sortByDate()
	questions = paginate(objects_list, request)
	context = {'questions' : questions, 'title' : 'Ask Malyshev'}
	return(render(request,"index.html", context))
	#return HttpResponse(request)

def login(request):
	#if request.user.is_authenticated():
		#return redirect('personal_page')
	if request.method=="POST":
		form = LoginForm(request.POST, request.FILES)
		print form
		if form.is_valid() and form.log_in():
			user = User.objects.get(username = form.cleaned_data['login'])
			print "login success"
			authorization(request, user)
			return redirect('personal_page')
		else:
			print form.errors
	form = LoginForm()
	context = {'title' : 'Ask Malyshev', 'form' : form}
	return render(request, "login.html", context)


#{{form.as_table}}
def signup(request):
	if request.method=="POST":
		form = RegistrationForm(request.POST, request.FILES)
		print form
		if form.is_valid() and form.authorization_conditions_are_complete():
			#TODO: create user
			user = form.save()
			authorization(request, user)
			print 'register success'
			return redirect('personal_page')
		print 'Save not success'
		print form.errors
	else:
		form = RegistrationForm()
	context = {'title' : 'Ask Malyshev', 'form' : form}
	return render(request, "signup.html", context)

def ask(request):
	if request.method=="POST":
		form = New_question_Form(request.POST, request.FILES)
		if form.is_valid():
			question = form.save(request.user)
			print 'success new question add'
			return redirect('question', question.id)
		print 'not success add new question'
		print form.errors
	else:
		form = New_question_Form()
	context = {'title' : 'Ask Malyshev', 'form' : form}
	return(render(request,"new-question.html", context))

def logout(request):
	print 'user logut'
	deAuthorization(request)
	return JsonResponse(dict(status='success'))

@login_required(login_url='login')
def personal_page(request):
	user = request.user
	print user.username
	if request.method=="POST":
		form =  ProfileForm(request.POST, request.FILES)
		if form.is_valid():
			user.avatar = form.cleaned_data['avatar']
			user.save()
			print 'Save success'
		else:
			print 'Save not success'
	form = ProfileForm()
	form.fields['login'].initial = user.username
	form.fields['nick'].initial = user.nick
	form.fields['email'].initial = user.email
	context = {'title' : 'Ask Malyshev', 'user' : user, 'form' : form}
	return(render(request,"presonal_page.html", context))

def question(request, qid):
	if request.method=="POST":
		form =  New_answer_form(request.POST, request.FILES)
		if form.is_valid():
			print "Correct answer"
			answer = form.make_answer(request.user, qid)
			question = Question.objects.get(pk=qid)
			context = {'answerer' : request.user, 'question' : question, "answer" : answer}
			requests.post('http://localhost:8888/publish/', data=dict(uid=qid, msg="New message created"))
			return(render(request,"answer.html", context))
		else:
			print "not correct answer"
			HttpResponse("not correct answer")
	else:
		result = re.search(r'(\d)+', request.path_info)
		if result != None:
			id = result.group(0)
		else:
			id = str(1)
		question = Question.objects.get(pk=id)
		objects_list = Answer.objects.answersOnQuestion(id)
		answers = paginate(objects_list, request)
		form = New_answer_form()
		if request.user.is_authenticated():
			chanal = question.id + "new_questions"
		else:
			chanal = datetime.datetime.now()
		context = {'answers' : answers, 'title' : 'Ask Malyshev', 'question' : question, 'questions' : answers, "form" : form, "user" : request.user, "chanal" : chanal}
		return(render(request,"question.html", context))
	
def searchByTag(request):
	tag = request.GET.get('tag')
	objects_list = Question.objects.questionsByTag(tag)
	questions = paginate(objects_list, request)
	context = {'questions' : questions, 'title' : 'Ask Malyshev', 'searchTag':tag}
	return(render(request,"listByTag.html", context))

def hot(request):
	objects_list = Question.objects.bestQuestions()
	questions = paginate(objects_list, request)
	context = {'questions' : questions, 'title' : 'Ask Malyshev'}
	return(render(request,"hot.html", context))

def getPostParameters(request):
	output = ['<p>WSGI!</p>']
	output.append('Hello world!')
	output.append('<br>')
	output.append('Post:')
	output.append('<form method="post" ')
	output.append('action="http://localhost/getPostParameters">')
	output.append('<input type="text" name = "test">')
	output.append('<input type="submit" value="Send">')
	output.append('</form>')
	if request.META['SERVER_PORT'] == '8080':
		if request.META['REQUEST_METHOD'] == 'POST':
			output.append('<h1>Post data:</h1>')
			for key, val in request.POST.iteritems():
				output.append(key + ' = ' + val)
				output.append('<br>')
		if request.GET:
			output.append('<h1>Get data:</h1>')
			for key in request.GET.keys():
				val = request.GET.get_list(key)
			#for key, val in request.GET.iteritems()::
				output.append(key + ' = ' + val)
				output.append('<br>')
		output.append(request.POST)
	return HttpResponse(output)

def vote(request):
	try:
		qid = int(request.POST.get('qid'))
	except:
		return JsonResponse(dict(error = 'bad question id'))
	vote = request.POST.get('vote')
	question = Question.objects.get(pk=qid)
	if not Like.objects.filter(question__id = qid, user__id = request.user.id):
		like = Like()
		like.user = request.user
		like.question = question
		like.assessment = 0
	else:
		like = Like.objects.get(question__id = qid, user__id = request.user.id)
	print like
	if vote == 'inc':
		if like.assessment <= 0:
			question.ratin += 1
			like.assessment += 2
			like.save()
			question.save()
		else:
			return JsonResponse(dict(error = "already inc"))
	if vote == 'dec':
		if like.assessment >= 0:
			question.ratin -= 1
			like.assessment -= 2
			like.save()
			question.save()
		else:
			return JsonResponse(dict(error = "already dec"))
	return JsonResponse(dict(ok=1, rating = question.ratin))

def correct(request):
	try:
		qid = int(request.POST.get('qid'))
	except:
		return JsonResponse(dict(error = 'bad question id'))
	try:
		aid = int(request.POST.get('aid'))
	except:
		return JsonResponse(dict(error = 'bad answer id'))
	answer = Answer.objects.get(pk=aid)
	question = Question.objects.get(pk=qid)
	old_correct_answer = Answer.objects.filter(question_id = qid, correct = True)
	if question.asking != request.user:
		return JsonResponse(dict(error = 'not asking'))
	if not old_correct_answer:
		answer.correct = True;
		answer.save()
		return JsonResponse(dict(ok=1, new_correct_answer_id = aid))
	old_correct_answer = Answer.objects.get(question_id = qid, correct = True)
	if old_correct_answer == answer:
		return JsonResponse(dict(error = 'already correct answer'))
	old_correct_answer.correct = False
	old_correct_answer.save()
	answer.correct = True
	answer.save()
	return JsonResponse(dict(ok=1, new_correct_answer_id = aid))