# -*- coding: utf-8 -*-
import requests
import nltk
import json
import os
import re
import traceback 
import six

from nltk import sent_tokenize, ne_chunk, pos_tag, word_tokenize
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
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

	def get(self, request):
	    # return 
	    return TemplateResponse(request, 'index.html', {})
	    
	@csrf_exempt
	def post(self, request):
	    # return keyword
	    texto_input = request.POST.get("texto", "")
	    
	    sentences = texto_input
	    l = []
	    toktok = ToktokTokenizer()
	    f = open(os.path.join(settings.BASE_DIR, 'stop_words.txt'), encoding='utf-8')
	    line = f.readline()
	    cnt = 1
	    stopwords_list = []
	    while line:
	    	line = f.readline()
	    	line = line.rstrip('\n')
	    	cnt += 1
	    	stopwords_list.append(line)

	    ##print(stopwords_list)

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

	    #print(unique_list)
	    
	    temp3 = []
	    for x in l: 
	    	if l.count(x) > 1: temp3.append(x)
	    temp3 = set(temp3)   
	    obj = {
	      'data': str(list(temp3)), 
	    } 
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
	
		

class TestClass(View):
	"""docstring for MainClass"""
	def get(self, request):
		from nltk.chunk import conlltags2tree, tree2conlltags
		main = MainClass()
		url = "https://www.infobae.com/sociedad/2019/11/01/una-mujer-denuncio-que-su-hija-fue-discriminada-y-que-desde-el-colegio-la-acusaron-de-buscar-fama-por-ser-actriz-porno/"
		texto = main.extracttext(url)
		sentences = json.loads(texto)
		sentences = sentences["data"]
		sentences = """
		Elon Musk has shared a photo of the spacesuit designed by SpaceX. This is the second image shared of the new design and the first to feature the spacesuit’s full-body look.
		"""
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
			word = re.sub('\W+', '', word)
			word = word.replace(">", "")
			return word

		nnp = False
		for n in ne_tree:
			#print(n[1])
			token = []
			if n[1] in ("NNP", "NN", "NNS"):
				if nnp: 
					print("true")
					print(n[0])
					nnp = False
					last_str = without_nnp.pop()
					
					str_words = n[0]
					str_words = clean(str_words)

					if str_words.lower() not in stopwords_list: 
						ne_tree_without_nnp.append(last_str + " " + str_words)
					else: nnp = False
				else: 
					print("false")

					print(n[0])
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

		iob_tagged = tree2conlltags(ne_tree)
		data = {"data": set(ne_tree_without_nnp)} # without_nnp, ne_tree_without_nnp
		return TemplateResponse(request, 'test.html', data)
		

class RakeTest(View):
	def get(self, request):
		import RAKE
		stop_dir = "stop_words.txt"
		rake_object = RAKE.Rake(stop_dir)
		text = """El litio es un elemento químico necesario para la composición de las baterías de los automóviles eléctricos y de gran importancia para la industria automovilística del futuro.
Bolivia posee reservas estimadas en 21 millones de toneladas de litio, de las más grandes del mundo. La mayor parte de ellas se sitúan en el salar de Uyuni y en menor proporción en los yacimientos de Coipasa y Pastos Grandes, según un estudio del gobierno boliviano.
Si bien Mujica dijo que no tiene pruebas para afirmar que detrás del golpe de Estado en Bolivia exista un interés por dicho elemento químico, de todos modos planteó su sospecha.
“Para mí es un golpe de Estado, sin vueltas, porque hay un ultimátum del Ejército”, dijo Mujica este lunes 11.
Cuestionó -en declaraciones a Televisión Nacional de Uruguay \(TNU\)- que después de que Evo Morales anunció el nuevo evento electoral, “la maquinaria golpista no se detuvo”.
Al ser consultado si Morales se equivocó o tuvo responsabilidad en los hechos, respondió que “todo eso puede ser, pero no justifica el linchamiento”.
“Bolivia es muy rica, se dice que tiene el 70% del material imprescindible para hacer las nuevas baterías. Todos sabemos que en el mundo hay un cambio energético. No estoy acusando, porque no tengo pruebas, estoy desconfiando, por la historia”.
Agregó que “el viejo liberalismo está enfermo, está hackeado, porque el neoliberalismo no tiene ninguna cortapisa de aliarse con actitudes que son fascistoides”.
Por su parte, Topolansky dijo que comparte la declaración de la Cancillería uruguaya en la que se habla de “quiebre del Estado de Derecho, que forzó la salida del poder del presidente Morales y que sumió al país en el caos y la violencia”.
“Bolivia es de los países de Latinoamérica que tiene mejor crecimiento, menor inflación, además descendió la pobreza y la indigencia en un 25%, recuperó los hidrocarburos y ha comenzado a explotar el litio, considerado el mineral del futro”, remarcó Topolansky.
Agregó. “Es un país que está en avance. Lamento en el alma estos sucesos y esperemos que no tengan costos de vida”.
Destacó que Evo Morales, al igual que Fernando Lugo en Paraguay, tomó una actitud muy madura. “En un momento dado determinó que su permanencia en el gobierno podía significar un costo en vidas y se retiró, aunque ello no fuera lo más justo”.
El gobierno uruguayo manifestó su consternación por el quiebre del Estado de derecho producido en…
El ex presidente de la República, José Mujica, participo de una cena de bienvenida del Grupo de Puebla, que se reúne este fin de semana en Buenos Aires, Argentina. También asistieron los ex presidentes: Dilma Rousseff \(Brasil\), Ernesto Samper...
El ex presidente de la República, José Mujica, expresó que la liberación de Luiz Inácio Lula da Silva debe ser tomada como una fiesta para la tolerancia, tanto en Brasil como en nuestra América.
Junto a Yamandú Orsi y otros referentes, José Mujica irá con todo para lograr el cuarto gobierno del Frente Amplio.
El Partido Por la Victoria del Pueblo PVP – Espacio 567 exigirá la renuncia de Gabriela Fulco como presidenta del Instituto Nacional de Inclusión Social Adolescente \(INISA\) quien se manifestó a favor del servicio militar obligatorio para...
Este miércoles será la última oportunidad para los dos candidatos para debatir frente a frente, a fin de convencer a los votantes indecisos o de robarle algunos votos a su contrincante."""
		keywords = rake_object.run(text)
		data = {"data": set(keywords)} # without_nnp, ne_tree_without_nnp
		return TemplateResponse(request, 'test.html', data)




def db(request):

    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
