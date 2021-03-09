# -*- coding: utf-8 -*-
import requests
import nltk
import json
import os
import re
import traceback 
import six
import operator
import RAKE

from nltk import sent_tokenize, ne_chunk, pos_tag, word_tokenize
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.stem import SnowballStemmer

nltk.data.path.append('./nltk_data/')

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View


#from .models import Greeting
from django.conf import settings

# Create your views here.
class MainClass(View):
	"""docstring for MainClass"""
	def extracttext(self, url):
		data = {"url":url}
		url = "http://extracttextpython.appspot.com/api/"
		r = requests.post(url, data=data, allow_redirects=True)
		return r.content

	def stopWord(text):
		#
		pass
		# sentences = texto
		# l = []
		# toktok = ToktokTokenizer()
	 	#f = open(os.path.join(settings.BASE_DIR, 'stop_words.txt'), encoding='utf-8')
	 	#line = f.readline()
	 	#cnt = 1
	 	#stopwords_list = []
	 	#while line:
	 	#line = f.readline()
	 	#line = line.rstrip('\n')
	 #    	cnt += 1
	 #    	stopwords_list.append(line)

	 #    ##print(stopwords_list)

	 #    for sent in sent_tokenize(sentences, language='spanish'):
	 #    	token = []
	 #    	tok = toktok.tokenize(sent)
	 #    	for to in tok:
	 #    		to = to.lower()
	 #    		to = to.replace("<br>", "")
	 #    		to = re.sub('\W+', '', to)
	 #    		if to not in stopwords_list:
	 #    			token.append(to)
	 #    	l.extend(token)
	    
	 #    l.sort()
	 #    unique_list = list(set(l))

	 #    #print(unique_list)
	    
	 #    temp3 = []
	 #    for x in l: 
	 #    	if l.count(x) > 1: temp3.append(x)
	 #    temp3 = set(temp3)   
	 #    obj = {
	 #      'data': str(list(temp3)), 
	 #    } 
	 #    dump = json.dumps(obj)
	 #    return HttpResponse(dump, content_type='application/json')

	def get(self, request):
	    # return 
	    return TemplateResponse(request, 'index.html', {})
	    
	@csrf_exempt
	def post(self, request):
	    # return keyword
	    if 'text' in self.request.POST:
	    	texto = self.request.POST["text"]

	    sentences = texto
	    l = []
	    toktok = ToktokTokenizer()
	    # sr = stopwords.words('spanish')
	    f = open(os.path.join(settings.BASE_DIR, 'stop_words.txt'), encoding='utf-8')
	    line = f.readline()
	    cnt = 1
	    # guardo los stopwords en una lista 
	    stopwords_list = []
	    while line:
	    	line = f.readline()
	    	line = line.rstrip('\n')
	    	cnt += 1
	    	stopwords_list.append(line)

	    ne_tree = pos_tag(word_tokenize(sentences), lang='eng')
	    ne_tree_without_nnp = []
	    without_nnp = []
	    #iob_tagged = tree2conlltags(ne_tree)
	    #data = {"data": ne_tree}
	    #return TemplateResponse(request, 'test.html', data)
	    def clean(word):
	    	word = word.replace("<br>", "")
	    	word = word.replace(">", "")
	    	word = re.sub('\W+', '', word)
	    	return word

	    nnp = False
	    for n in ne_tree:
	    	token = []
	    	if n[1] in ("NNP"): #"NNS", "NN"
	    		if nnp:
	    			nnp = False
	    			last_str = without_nnp.pop()
	    			str_words = n[0]
	    			str_words = clean(str_words)
	    			if str_words.lower() not in stopwords_list: 
	    				ne_tree_without_nnp.append(last_str + " " + str_words)
	    			else: nnp = False
	    		else:
	    			without_nnp_str_words = n[0]
	    			without_nnp_str_words = clean(without_nnp_str_words)
	    			if without_nnp_str_words.lower() not in stopwords_list: 
	    				if without_nnp_str_words.strip():
	    					without_nnp.append(without_nnp_str_words)
	    					print(without_nnp)

	    				nnp = True
	    	else: nnp = False

	    for sent in sent_tokenize(sentences, language='spanish'):
	    	token = []
	    	tok = toktok.tokenize(sent)
	    	for to in tok:
	    		to = to.lower()
	    		to = to.replace("<br>", "")
	    		to = re.sub('\W+', '', to)
	    		if to not in stopwords_list: token.append(to)
	    	l.extend(token)
	    
	    obj = {'data': str(list(set(ne_tree_without_nnp)))}
	    dump = json.dumps(obj)
	    return HttpResponse(dump, content_type='application/json')


class ApiClass(View):
	"""docstring for ApiClass"""
	@csrf_exempt
	def post(self, request):
	    # return keyword
	    try:
	    	texto = request.POST.get("text", "")
	    	print(texto)
	    except:
	    	error = traceback.format_exc()
	    	dump = json.dumps(error)
	    	return HttpResponse(dump, content_type='application/json')	    

	    sentences = texto
	    l = []
	    toktok = ToktokTokenizer()
	    # sr = stopwords.words('spanish')
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
	    
	    temp3 = []
	    for x in l: 
	    	if l.count(x) > 1: temp3.append(x)
	    temp3 = set(temp3)   
	    obj = {
	      'data': str(list(temp3)), 
	    } 
	    dump = json.dumps(obj)
	    return HttpResponse(dump, content_type='application/json')
	
		
class NameExtractClass(View):
	"""docstring for MainClass"""
	def get(self, request):
		main = MainClass()
		url = "https://ladiaria.com.uy/articulo/2019/11/dirigente-de-cabildo-abierto-es-investigado-por-la-justicia-por-convocar-a-crear-un-escuadron-de-la-muerte/"
		texto = main.extracttext(url)
		sentences = json.loads(texto)
		sentences = sentences["data"]
		sentences = """Cabalgata y juegos de toro en Atalaya"""
		l = []
		toktok = ToktokTokenizer()
		# sr = stopwords.words('spanish')
		f = open(os.path.join(settings.BASE_DIR, 'stop_words.txt'), encoding='utf-8')
		line = f.readline()
		cnt = 1
		# guardo los stopwords en una lista 
		stopwords_list = []
		while line:
			line = f.readline()
			line = line.rstrip('\n')
			cnt += 1
			stopwords_list.append(line)

		ne_tree = pos_tag(word_tokenize(sentences), lang='eng')
		ne_tree_without_nnp = []
		without_nnp = []
		#iob_tagged = tree2conlltags(ne_tree)
		#data = {"data": ne_tree}
		#return TemplateResponse(request, 'test.html', data)
		def clean(word):
			word = word.replace("<br>", "")
			word = word.replace(">", "")
			word = re.sub('\W+', '', word)
			return word

		nnp = False
		a = []
		prev_word = ''
		for n in ne_tree:
			token = []
			str_words = n[0]
			str_words = clean(str_words)
			print(n[0])
			print(n[1])
			print(' ')
			if n[1] in ("NNP", "VBZ","NN", "FW"):
				if str_words.lower() not in stopwords_list: 
					if n[1] == "NNP":
						a.append(str_words)
					ne_tree_without_nnp.append(str_words)
			else: 
				if str_words.lower() not in stopwords_list: 
					str_words = ' '.join(a)
					ne_tree_without_nnp.append(str_words)
				if len(a) > 0:
					str_words = ' '.join(a)
					ne_tree_without_nnp.append(str_words)
				print(a)
				print(' ')
				a = []

		for sent in sent_tokenize(sentences, language='spanish'):
			token = []
			tok = toktok.tokenize(sent)
			for to in tok:
				to = to.lower()
				to = to.replace("<br>", "")
				to = re.sub('\W+', '', to)
				if to not in stopwords_list: token.append(to)
			l.extend(token)

		iob_tagged = tree2conlltags(ne_tree)

		ne_tree_without_nnp = [e for e in ne_tree_without_nnp if e != '']
		l = []
		for y in ne_tree_without_nnp:
			two_words = y if len(y.split(' ')) > 1 else ''
			if not two_words:
				length = len([e for e in ne_tree_without_nnp if e == y])
				l.append(y if length > 2 else '')
			else: l.append(y)
			

		data = {"data": set(ne_tree_without_nnp)} # without_nnp, ne_tree_without_nnp
		data = {"data": str(set(ne_tree_without_nnp))} # without_nnp, ne_tree_without_nnp
		dump = json.dumps(data)
		return HttpResponse(dump, content_type='application/json')
		#return TemplateResponse(request, 'test.html', data)

	def post(self, request):
		main = MainClass()
		#print('values')
		#print(request.body)
		#print(' ')
		body_unicode = request.body.decode('utf-8')
		body_unicode = json.loads(body_unicode)
		#print(body_unicode[0]['Headline'])
		#print(type(body_unicode))
		#print(' ')
		#body = json.loads(body_unicode)
		#print(body['data'])
		#print(body['Id_URL'])

		#print(' ')
		#url = "https://ladiaria.com.uy/articulo/2019/11/dirigente-de-cabildo-abierto-es-investigado-por-la-justicia-por-convocar-a-crear-un-escuadron-de-la-muerte/"
		#texto = main.extracttext(url)
		#sentences = json.loads(texto)
		#sentences = sentences["data"]
		#sentences = body_unicode #body['data']
		dump = []
		for senten in body_unicode:
			#print('sentence')
			#print(senten)
			sentences = senten['Headline']
			#print(' ')
			l = []
			toktok = ToktokTokenizer()
			# sr = stopwords.words('spanish')
			f = open(os.path.join(settings.BASE_DIR, 'stop_words.txt'), encoding='utf-8')
			line = f.readline()
			cnt = 1
			# guardo los stopwords en una lista 
			stopwords_list = []
			while line:
				line = f.readline()
				line = line.rstrip('\n')
				cnt += 1
				stopwords_list.append(line)

			ne_tree = pos_tag(word_tokenize(sentences), lang='eng')
			ne_tree_without_nnp = []
			without_nnp = []
			#iob_tagged = tree2conlltags(ne_tree)
			#data = {"data": ne_tree}
			#return TemplateResponse(request, 'test.html', data)
			def clean(word):
				word = word.replace("<br>", "")
				word = word.replace(">", "")
				word = re.sub('\W+', '', word)
				return word

			nnp = False
			a = []
			prev_word = ''
			for n in ne_tree:
				token = []
				str_words = n[0]
				str_words = clean(str_words)
				#print(n[0])
				#print(n[1])
				#print(' ')
				if n[1] in ("NNP", "VBZ","NN", "FW"):
					str_words = str_words.lower()
					str_words = str_words.strip()
					if str_words.lower() not in stopwords_list: 
						stemmer = SnowballStemmer('spanish')
						if n[1] in ("VBZ", "FW"):
							str_words = stemmer.stem(str_words)
						if n[1] == "NNP":
							a.append(str_words)
						ne_tree_without_nnp.append(str_words)

				else: 
					if str_words.lower() not in stopwords_list: 
						str_words = ' '.join(a)
						ne_tree_without_nnp.append(str_words)
					if len(a) > 0:
						str_words = ' '.join(a)
						ne_tree_without_nnp.append(str_words)
					#print(a)
					#print(' ')
					a = []

			for sent in sent_tokenize(sentences, language='spanish'):
				token = []
				tok = toktok.tokenize(sent)
				for to in tok:
					to = to.lower()
					to = to.replace("<br>", "")
					to = re.sub('\W+', '', to)
					if to not in stopwords_list: token.append(to)
				l.extend(token)

			iob_tagged = tree2conlltags(ne_tree)

			ne_tree_without_nnp = [e for e in ne_tree_without_nnp if e != '']
			l = []
			for y in ne_tree_without_nnp:
				two_words = y if len(y.split(' ')) > 1 else ''
				if not two_words:
					length = len([e for e in ne_tree_without_nnp if e == y])
					l.append(y if length > 2 else '')
				else: l.append(y)
				
			senten['keys'] = list(set(ne_tree_without_nnp))
			senten['Similar'] = []
			senten['SimilarKeys'] = []
			senten['SourceSimilar'] = []
			senten['SharedCountSimilar'] = []
			senten['ReachSimilar'] = []
			senten['ShowItem'] = 'true'

			#senten['Percentage'] = []
			
			# without_nnp, ne_tree_without_nnp
			dump.append(senten)
		#dump = json.dumps(dump)
		#print(' ')
		#print('dump ')
		#print(dump)
		#dump = list(dump)
		#print(type(dump))
		#print(dump)
		dataSimilar = dump
		def check_similar(dump):
			dataResponse = {}
			c = 0
			keysUsed = []
			for i in dump:
				c += 1
				copyI = i.copy()
				#if c == 40:	break
				dataResponse[i["Id_URL"]] = copyI#hago una copia para que no se tome por referencia y me cague toda la compu
				for e in dump:
					if i['Id_URL'] != e['Id_URL']:#no hagas nada si sos el mismo que ayer
						if True:
							diferentKeys = list(set(i["keys"]) & set(e["keys"])) #filteredList
							if len(diferentKeys) >= 2:
								porcentaje = (float(len(diferentKeys)) / len(e['keys'])) * 100
								#print(' ')
								#print(porcentaje)
								#print(i["Id_URL"], e['Id_URL'])
								if porcentaje > 10:
									if e["Id_URL"] not in copyI["SimilarKeys"] and (e["Id_URL"] not in keysUsed):
										#copyI["Similar"].append(e.copy())
										copyI["SimilarKeys"].append(e["Id_URL"])

										if e["Source"] not in copyI["SourceSimilar"]:
											copyI["SourceSimilar"].append(e["Source"])
										if len(copyI["SharedCountSimilar"]) == 0:
											copyI["SharedCountSimilar"].append(i["Share_Count"] + e["Share_Count"])#Twitter_Social_Echo
										else: copyI["SharedCountSimilar"].append(i["Share_Count"])
										copyI["ReachSimilar"].append(e["Reach"])
										#copyI["Percentage"].append(porcentaje)
										keysUsed.append(e["Id_URL"])
									
			return dataResponse
		
		#print(' ')
		#print(' ')
		#print('diump')
		getdata = check_similar(dump)
		
		#print(getdata)
		responseDump = []	
		for i in getdata:
			responseDump.append(getdata[i])

		#print(responseDump)
		responseDump2 = []
		c = 0
		for i in responseDump:
			i['Opening_Text'] = i['Opening_Text'].replace('"', '')
			i['Headline'] = i['Headline'].replace('"', '')
			i['Headline'] = i['Headline'].replace('“', '')
			i['Headline'] = i['Headline'].replace('”', '')
			i['Hit_Sentence'] = i['Hit_Sentence'].replace('"', '')
			
			#print(i['Headline'].replace('"', ''))
			responseDump2.append(responseDump[c])
			c += 1

		responseDump = str(responseDump2)
		#print('FIN')
		#responseDump = json.dumps(responseDump)

		return HttpResponse(responseDump, content_type='application/json')


class RakeTest(View):
	def get(self, request):
		stop_dir = "stop_words.txt"
		rake_object = RAKE.Rake(stop_dir)
		text = """Comisionado Jeremías Urieta, nuevo director del SENAN"""
		#main = MainClass()
		#url = "http://www.lr21.com.uy/deportes/1415084-seleccion-uruguay-futbol-hungria-argentina-israel-crisis"
		#texto = main.extracttext(url)
		#sentences = json.loads(texto)
		#text = sentences["data"]
		keywords = rake_object.run(text) # minCharacters = 1, maxWords = 10, minFrequency = 2
		words_list = []
		for i in keywords:
			if i[1] >= 2:
				word = i[0]
				word = word.replace("<br>", "")
				word = word.replace(">", "")
				word = word.replace('"', '')
				word = word.replace("<", "")
				word = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ", word)
				word = re.sub("(\\d|\\W)+"," ", word)
				word = word.lstrip('\"')
				word = word.rstrip('\"')
				word = re.sub(r"^\s+", "", word)
				word = re.sub(r"\s+$", "", word)
				word = ''.join(c for c in word if c not in '"')
				#ord = re.sub("^\"(.+)\"$", '', word)
				#if word.startswith('"') and word.endswith('"'): word = word[1:-1]
				#if word.startswith('"'): word = word[1:]
				#if word.endswith('"'): word = word[:-1]
				#print(str(word))
				#print("-----------dsdsads-------------------------------------------")
				if word not in words_list:
					words_list.append(word)
		data = {"data": words_list} # without_nnp, ne_tree_without_nnp
		return TemplateResponse(request, 'test.html', data)

	def post(self, request):
		try:
			stop_dir = "stop_words.txt"
			rake_object = RAKE.Rake(stop_dir)
			# get text from call
			text = self.request.POST["text"]
			#main = MainClass()
			#url = "http://www.lr21.com.uy/deportes/1415084-seleccion-uruguay-futbol-hungria-argentina-israel-crisis"
			#texto = main.extracttext(url)
			#sentences = json.loads(texto)
			#text = sentences["data"]

			keywords = rake_object.run(text, minCharacters = 2, maxWords = 3, minFrequency = 1)
			words_list = []
			for i in keywords:
				if i[1] > 2:
					word = i[0] 
					word = word.replace("<br>", "")
					word = word.replace(">", "")
					word = word.replace("\"", "")
					word = word.replace("<", "")
					word = re.sub("&lt;/?.*?&gt;"," &lt;&gt; ", word)
					word = re.sub("(\\d|\\W)+"," ", word)
					word = word.lstrip('\"')
					word = word.rstrip('\"')
					word = re.sub(r"^\s+", "", word)
					word = re.sub(r"\s+$", "", word)
					#word = re.sub('\W+', '', word)
					words_list.append(word)
			data = {"data": str(set(words_list))} # without_nnp, ne_tree_without_nnp
			dump = json.dumps(data)
			return HttpResponse(dump, content_type='application/json')
		except:
			error = traceback.format_exc()
			obj = {'data': error}
			dump = json.dumps(obj)
			return HttpResponse(dump, content_type='application/json')


