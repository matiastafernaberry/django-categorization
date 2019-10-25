# -*- coding: utf-8 -*-
import requests
import nltk
import json
import os
from nltk import sent_tokenize
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords


from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from django.conf import settings

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    data = {"url":"https://www.elpais.com.uy/informacion/politica/larranaga-mal-allanamientos-nocturnos-plantea.html"}
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
    	#print(line.strip())
    	line = f.readline()
    	line = line.rstrip('\n')
    	#str(line, 'utf-8')
    	cnt += 1
    	stopwords_list.append(line)

    #print(stopwords_list)
    for sent in sent_tokenize(sentences, language='spanish'):
    	token = []
    	tok = toktok.tokenize(sent)
    	for to in tok:
    		#to = str(to, 'unicode-escape')
    		#str(to, 'utf-8')
    		print(to)
    		if to.lower() not in stopwords_list:
    			token.append(to.lower())

    	l.append(token)
    l = str(l)
    	
    #[toktok.tokenize(sent) for sent in sent_tokenize(sentences, language='spanish')]
    return HttpResponse('<pre>' + l + '</pre>')
    #return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
