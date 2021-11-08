from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .forms import IntentQuestions
from .utils import make_intents, train_chatbot, chatbot
import os
import json

on_training = []

def home(request):
    return render(request, 'chatbot/home.html', {'title':'chatbot'})

@login_required
def personal_details(request):
	if request.method=="POST":
		form = IntentQuestions(request.POST)
		if form.is_valid():
			make_intents(form.cleaned_data, request.user.username)
			messages.success(request, f'Your personal details successfully get saved! You are now able to train your chatbot')
			return redirect('chatbot-train')
	else:
		form = IntentQuestions()
	return render(request, 'chatbot/personal_details.html', {'title':'personal_details', 'form':form})

@login_required
@csrf_exempt
def train(request):
	path = os.path.abspath(os.path.dirname(__file__))
	path = os.path.join(path, 'static/chatbot/intents/personal_intents', f'{request.user.username}_personal_intent.json')
	if not os.path.isfile(path):
		messages.warning(request, 'You need to enter some of your personal details before training the chatbot.')
		return redirect('chatbot-personal_details')
	if request.method=="POST":
		if request.user.username in on_training:
			return JsonResponse({'status': 'Your model has been training, kindly wait for few minutes.'})
		on_training.append(request.user.username)
		if train_chatbot(request.user.username):
			on_training.remove(request.user.username)
			return JsonResponse({'status': 'trained sucessfully'})
		on_training.remove(request.user.username)
	return render(request, 'chatbot/train.html', {'title':'train_chatbot'})

# @require_http_methods(["POST"])
# def train_process(request):
# 	path = os.path.abspath(os.path.dirname(__file__))
# 	path = os.path.join(path, 'static/chatbot/intents/personal_intents', f'{request.user.username}_personal_intent.json')
# 	if not os.path.isfile(path):
# 		return JsonResponse({'error': 'Please re-train your model. If problem does not solve, contact us as soon as possible.'})
# 	train_chatbot(request.user.username)
# 	return JsonResponse({'status': 'trained sucessfully'})

@require_http_methods(["POST"])
@csrf_exempt
def chat(request, username):
	path = os.path.abspath(os.path.dirname(__file__))
	path = os.path.join(path, 'static/chatbot/models', f'{username}')
	if os.path.isdir(path) and os.path.isfile(os.path.join(path, 'data.pickle')) and os.path.isfile(os.path.join(path, 'model.tflearn.meta')):
		data = json.loads(request.body.decode('utf-8'))
		rply = chatbot(data.get("query"), username)
		return JsonResponse({'name':username, 'query':data.get("query"), 'reply': rply})	
	return JsonResponse({'error': 'Please re-train your model. If problem does not solve, contact us as soon as possible.'})