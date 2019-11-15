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
			#print(n[1])
			token = []
			if n[1] in ("NNP"): #"NNS", "NN"
				if nnp: 
					#print("true")
					#print(n[0])
					#nnp = False
					if without_nnp: last_str = without_nnp.pop()
					else: last_str = ""
					str_words = n[0]
					str_words = clean(str_words)
					word = last_str + " " + str_words

					if str_words.lower() not in stopwords_list: 
						ne_tree_without_nnp.append(word)
						f = open("demofile2.txt", "a")
						f.write((word.lower()).strip() + "\n")
						f.close()
					else: nnp = False
				else: 
					#print("false")
					#print(n[0])
					without_nnp_str_words = n[0]
					without_nnp_str_words = clean(without_nnp_str_words)
					if without_nnp_str_words.lower() not in stopwords_list: 
						if without_nnp_str_words.strip():
							without_nnp.append(without_nnp_str_words)
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

		iob_tagged = tree2conlltags(ne_tree)
		data = {"data": set(ne_tree_without_nnp)} # without_nnp, ne_tree_without_nnp
		return TemplateResponse(request, 'test.html', data)


	def post(self, request):
		try:
			#main = MainClass()
			#url = "http://www.lr21.com.uy/deportes/1415084-seleccion-uruguay-futbol-hungria-argentina-israel-crisis"
			#texto = main.extracttext(url)
			#sentences = json.loads(texto)
			#sentences = sentences["data"]
			#sentences = """
			#Elon Musk has shared a photo of the spacesuit designed by SpaceX. This is the second image shared of the new design and the first to feature the spacesuit’s full-body look.
			#"""
			sentences = self.request.POST["text"]
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
				#print(n[1])
				token = []
				if n[1] in ("NNP"): #"NNS", "NN"
					if nnp: 
						#print("true")
						#print(n[0])
						nnp = False
						last_str = without_nnp.pop()
						str_words = n[0]
						str_words = clean(str_words)
						str_words = last_str + " " + str_words
						if str_words.lower() not in stopwords_list: 
							ne_tree_without_nnp.append(str_words)
						else: nnp = False
					else: 
						#print("false")
						#print(n[0])
						without_nnp_str_words = n[0]
						without_nnp_str_words = clean(without_nnp_str_words)
						if without_nnp_str_words.lower() not in stopwords_list: 
							if without_nnp_str_words.strip():
								without_nnp.append(without_nnp_str_words)
								#print(without_nnp)

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
		except:
			error = traceback.format_exc()
			obj = {'data': error}
			dump = json.dumps(obj)
			return HttpResponse(dump, content_type='application/json')

class RakeTest(View):
	def get(self, request):
		stop_dir = "stop_words.txt"
		rake_object = RAKE.Rake(stop_dir)
		text = """El líder de Alianza Nacional Jorge Larrañaga señaló este lunes en una carta pública que hay “instituciones públicas que se deben a todos los uruguayos, que están actuando orgánicamente al compás del dictamen y las necesidades de la 'fuerza política'; sí, del Frente Amplio”, en referencia a la campaña contra el plebiscito que impulsa la iniciativa Vivir sin Miedo, que encabeza el senador nacionalista. En la carta, que se titula “Patoteros del poder” y que el legislador compartió en su cuenta de Twitter, Larrañaga señala al comienzo que su reforma “está bajo ataque del Frente Amplio algo esperable porque cuestiona una de sus mayores falencias, la falta de respuestas en materia de seguridad-, pero también, bajo taque de instituciones públicas que deberían actuar regidas por los códigos de neutralidad y decoro republicano y no por los designios frentistas”. Además, el senador planteó que si él “propone” realizar allanamientos nocturnos “está mal”. Pero, agregó, los “hechos” marcan que el presidente Tabaré Vázquez en 2006 en el Proyecto de Ley de Procedimiento Policial, también los incluía. José Mujica los propuso, Eduardo Bonomi, los propuso, y una cantidad de dirigentes de todas las orientaciones han mostrado su conformidad con la propuesta”. “Son permitidos en casi todo el mundo, solo Portugal tiene una prohibición similar a la de nuestra Constitución. Entonces, ¿están mal los allanamientos nocturnos o quien los plantea?”, agregó. El exprecandidato sostiene en el texto que el Frente Amplio ha construido “a lo largo de décadas” un “aparato cultural”, el cual “suele asistir al aparato político actuando en sintonía y coadyuvando a generar una hegemonía mediante un culto al pensamiento único, erigiéndose en jueces de lo moral y políticamente correcto”. A estas instituciones que apoyan la campaña contraria a la reforma les llama “agencias satélites de un proyecto político”. En tal sentido, se refiere a instituciones públicas como la Institución Nacional de Derechos Humanos (Inddhh), “emitiendo no uno sino dos pronunciamientos sin fundamentos contra la reforma” y también suma a su lista a centros de enseñanza públicos. Además, Larrañaga criticó que "instituciones" como la Universidad de la República (UdelaR) que “deberían inspirarse en un espíritu crítico, científico y riguroso, pasan a actuar como delegados de lujo de una postura partidista”. ntualmente nombra a la Facultad de Psicología, que divulgó el viernes una carta donde señala que la reforma Vivir sin Miedo "propone medidas que ponen en riesgo la vida plena de las y los habitantes del país, produciendo condiciones represivas que generan violencia, temor y sufrimiento mental”. Respecto a esta última expresión, Larrañaga respondió: “Sin palabras. No tienen pudor frente al disparate”. "No tienen derecho los que son coyuntural mayoría a excluir a otros. Eso pasa en algunas Facultades que hacen campaña. ¿Y los que tiene otra posición? Más aún, si no hubiera ningún estudiante, ningún profesor, ningún gremialista a favor de una posición, eso tampoco le da derecho a nadie a apropiarse de la Institución embanderándola con una postura determinada", dijo Larrañaga. Considera además “escandaloso” que las instituciones públicas “oficialicen una posición, que abandonen la neutralidad, atacando al principio de laicidad”. Además, manifestó que el “principal arsenal son los prejuicios y los falsos 'cucos' importados y no los argumentos. Se usan palabras, pero se reniega de los hechos”, esta última expresión, en referencia a los dichos del candidato presidencial Daniel Martínez durante el debate presidencial del 1° de octubre pasado ("hechos, no palabras"). """
		#main = MainClass()
		#url = "http://www.lr21.com.uy/deportes/1415084-seleccion-uruguay-futbol-hungria-argentina-israel-crisis"
		#texto = main.extracttext(url)
		#sentences = json.loads(texto)
		#text = sentences["data"]
		keywords = rake_object.run(text) # minCharacters = 1, maxWords = 10, minFrequency = 2
		words_list = []
		for i in keywords:
			if i[1] > 1:
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
				words_list.append(word)
		data = {"data": set(words_list)} # without_nnp, ne_tree_without_nnp
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



def db(request):

    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
