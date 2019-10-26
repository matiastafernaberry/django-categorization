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
    	cnt += 1
    	stopwords_list.append(line)

    #print(stopwords_list)
    for sent in sent_tokenize(sentences, language='spanish'):
    	token = []
    	tok = toktok.tokenize(sent)
    	for to in tok:
    		#print(to)
    		to = to.lower()
    		to = to.replace("<br>", "")
    		to = re.sub('\W+', '', to)
    		if to not in stopwords_list:
    			#print(to)
    			token.append(to)

    	l.extend(token)
    
    l.sort()
    
    #l = str(l)
    text = nltk.Text(str(l))
    #fdist = FreqDist(l)
    print("fdist:  ")
    print("  ----   ")
    print("  ----   ")
    #words = list(fdist.keys())
    #print(words)
    fdist = str(text)
    
    	
    #[toktok.tokenize(sent) for sent in sent_tokenize(sentences, language='spanish')]
    return HttpResponse('<p>' + str(l) + '</p>')
    #return render(request, "index.html")


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
