# -*- coding: utf-8 -*-
import requests
import nltk
import json
import os
import re 

from nltk import sent_tokenize
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
nltk.data.path.append('./nltk_data/')
from nltk import FreqDist


from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View


from .models import Greeting
from django.conf import settings

# Create your views here.
class MainClass(View):
	"""docstring for MainClass"""
	# def __init__(self, arg):
	# 	super(MainClass, self).__init__()
	# 	self.arg = arg

	def get(self, request):
	    # return HttpResponse('Hello from Python!')
	    data = {"url":"https://findesemana.ladiaria.com.uy/articulo/2019/10/una-mirada-desde-las-calles-de-santiago-de-chile/"}
	    url = "http://extracttextpython.appspot.com/api/"
	    r = requests.post(url, data=data, allow_redirects=True)
	    y = json.loads(str(r.text))
	    sentences = y["data"]
	    l = []
	    toktok = ToktokTokenizer()
	    #sr = stopwords.words('spanish')
	    f = open(os.path.join(settings.BASE_DIR, 'stop_words.txt'), encoding='utf-8')
	    line = f.readline()
	    cnt = 1
	    stopwords_list = []
	    while line:
	    	line = f.readline()
	    	line = line.rstrip('\n')
	    	cnt += 1
	    	stopwords_list.append(line)

	    for sent in sent_tokenize(sentences, language='spanish'):
	    	token = []
	    	tok = toktok.tokenize(sent)
	    	for to in tok:
	    		to = to.lower()
	    		to = to.replace("<br>", "")
	    		to = re.sub('\W+', '', to)
	    		if to not in stopwords_list:
	    			token.append(to)
	    	l.extend(token)
	    
	    l.sort()
	    #print("fdist4")
	    unique_list = list(set(l))
	    
	    #print(str(unique_list))
	    temp3 = []
	    for x in l: 
	    	if l.count(x) > 1: temp3.append(x)
	    #print(set(temp3))
	    temp3 = set(temp3)
	    #for i in l:
	    #l = str(l)
	    #text = nltk.Text(str(l))
	    #fdist = FreqDist(l)
	    #print("fdist:  ")
	    #print("  ----   ")
	    #print("  ----   ")
	    #words = list(fdist.keys())
	    #print(fdist)
	    #fdist = str(text)
	    #words = list(fdist.keys())
	    #print(words)
	    #print(fdist['derecho'])
	    #print("  ------end--------  ")
	    #[toktok.tokenize(sent) for sent in sent_tokenize(sentences, language='spanish')]
	    #request.response.headers['Content-Type'] = 'application/json'   
	    obj = {
	      'data': str(list(temp3)), 
	    } 
	    dump = json.dumps(obj)
	    return HttpResponse(dump, content_type='application/json')
	    

	@csrf_exempt
	def post(self, request):
		url = request.POST.get("url", "")
	    # return HttpResponse('Hello from Python!')
	    data = {"url":url}
	    url = "http://extracttextpython.appspot.com/api/"
	    r = requests.post(url, data=data, allow_redirects=True)
	    y = json.loads(str(r.text))
	    sentences = y["data"]
	    l = []
	    toktok = ToktokTokenizer()
	    #sr = stopwords.words('spanish')
	    f = open(os.path.join(settings.BASE_DIR, 'stop_words.txt'), encoding='utf-8')
	    line = f.readline()
	    cnt = 1
	    stopwords_list = []
	    while line:
	    	line = f.readline()
	    	line = line.rstrip('\n')
	    	cnt += 1
	    	stopwords_list.append(line)

	    for sent in sent_tokenize(sentences, language='spanish'):
	    	token = []
	    	tok = toktok.tokenize(sent)
	    	for to in tok:
	    		to = to.lower()
	    		to = to.replace("<br>", "")
	    		to = re.sub('\W+', '', to)
	    		if to not in stopwords_list:
	    			token.append(to)
	    	l.extend(token)
	    
	    l.sort()
	    unique_list = list(set(l))
	    
	    #print(str(unique_list))
	    temp3 = []
	    for x in l: 
	    	if l.count(x) > 1: temp3.append(x)
	    #print(set(temp3))
	    temp3 = set(temp3)   
	    obj = {
	      'data': str(list(temp3)), 
	    } 
	    dump = json.dumps(obj)
	    return HttpResponse(dump, content_type='application/json')


def db(request):

    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
