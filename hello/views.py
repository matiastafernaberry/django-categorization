# -*- coding: utf-8 -*-
import requests
import nltk
import json
import os
import re
import traceback 

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
		#sentences = """
		#	Este jueves 7 de noviembre, La Corte Suprema de Brasil decidió por seis votos contra cinco que la prisión de una persona condenada solamente en segunda instancia es inconstitucional, según informaron diversos medios de prensa brasileños.
		#	En el marco de la votación, entendieron que se debía modificar la jurisprudencia, los jueces: Marco Aurélio Mello, Rosa Weber, Ricardo Lewandowski, Gilmar Mendes, Celso de Mello, y el presidente del Supremo Tribunal Federal, José António Dias Toffoli.
		#	Mientras que se pronunciaron en contra: Alexandre de Moraes, Edson Fachin, Carmen Lúcia, Roberto Barroso y Luiz Fux.
		#	Hasta el momento, una sentencia de prisión debía comenzar a ser cumplida luego de que fuera confirmada por un tribunal de segunda instancia. De acuerdo con la nueva interpretación, la pena debería comenzar a cumplirse cuando el acusado haya agotado todos los recursos legales disponibles.
		#	A raíz de tal decisión, el ex presidente Lula da Silva podrá ser liberado, junto con casi 5.000 personas que se encuentran privadas de libertad por distintas causas.
		#	En tal sentido, el equipo de abogados del ex mandatario brasileño aseguró que solicitarán la “liberación inmediata” de Lula, según informó Folha de São Paulo.
		#	Se estima que Lula podría ser liberado la próxima semana. De todos modos el estudio de su caso continuará.
		#	Lula da Silva se encuentra en prisión, desde abril del año pasado, en una dependencia policial de la ciudad de Curitiba.
		#	El ex mandatario ha sido acusado de “corrupción” en el marco de la causa: “tríplex de Guarujá”.
		#	Había sido condenado a ocho años y diez meses de cárcel, acusado de “corrupción y lavado de dinero por haber recibido un apartamento de parte de la empresa constructora OAS, a cambio de contratos de obra con la petrolera estatal Petrobras”.
		#"""

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
		nnp = False
		for n in ne_tree:
			#print(n[1])
			token = []
			if n[1] == "NNP":
				if nnp: 
					nnp = False
					last_str = without_nnp.pop()
					
					str_words = n[0]
					str_words = str_words.replace("<br>", "")

					str_words = re.sub('\W+', '', str_words)
					str_words = str_words.replace(">", "")
					if str_words.lower() not in stopwords_list: 
						ne_tree_without_nnp.append(last_str + " " + str_words)
					else: nnp = False
				else: 
					without_nnp_str_words = n[0] 
					without_nnp_str_words = without_nnp_str_words.replace("<br>", "")
					without_nnp_str_words = re.sub('\W+', '', without_nnp_str_words)
					without_nnp_str_words = without_nnp_str_words.replace(">", "")
					if without_nnp_str_words.lower() not in stopwords_list: 
						if without_nnp_str_words.strip():
							without_nnp.append(without_nnp_str_words)
							nnp = True
			else: nnp = False



		for sent in sent_tokenize(sentences, language='spanish'):
			#print("ssssssssssssssssssssssssssssssssss")
			#print(sent)
			token = []
			tok = toktok.tokenize(sent)
			for to in tok:
				to = to.lower()
				to = to.replace("<br>", "")
				to = re.sub('\W+', '', to)
				if to not in stopwords_list: token.append(to)
			l.extend(token)


		iob_tagged = tree2conlltags(ne_tree)
		data = {"data": set(ne_tree_without_nnp)}
		return TemplateResponse(request, 'test.html', data)
		

def db(request):

    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
