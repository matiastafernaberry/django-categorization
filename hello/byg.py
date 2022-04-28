#!/usr/bin/env python3
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
import jinja2
import csv
import datetime
from datetime import datetime, timedelta

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
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from os import listdir
from os.path import isfile, join
import mysql.connector
import pandas as pd
from pandas import DataFrame


#from .models import Greeting
from django.conf import settings


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__).replace("views","")),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
)


class ApiGetDocumentsSharedCount7Class(View):
	"""docstring for MainClass"""
	# def get(self, request):
	# 	mypath = "hello/static/sfiles/"
	# 	import glob
	# 	files = list(filter(os.path.isfile, glob.glob(mypath + "*")))
	# 	files.sort(key=lambda x: os.path.getmtime(x))
	# 	print(files)
	# 	files.reverse()
	# 	fil = []
	# 	for i in files:
	# 		fil.append(i.replace('hello/static/sfiles/', ''))
	# 	return TemplateResponse(request, 'files.html', {'files': fil})

	def post(self, request):
		dataPost = request.body.decode('utf-8')
		dataPost = json.loads(dataPost)
		print(dataPost['similar'])
		#dataPostStr = ','.join(map(str, dataPost['similar']))
		try: dataPost = tuple(dataPost['similar'])
		except: dataPost = str(dataPost['similar'])
		#print(dataPostStr)
		cnx = mysql.connector.connect(user='admin', password='3y3w4tch20204dm1n',
            host='meltwater-dbcluster-instance-1.cffatgb5exir.us-west-2.rds.amazonaws.com',
            database='meltwater')
		cursor1 = cnx.cursor(buffered=True)
		if isinstance(dataPost, tuple):
			cursor1.execute("""SELECT DISTINCT( dsc.`URL`), dsc.`Date`, dsc.`Share_Count`, d.Id_URL 
				FROM DOCUMENTS_SHAREDCOUNT_TREND_7_DIAS as dsc, DOCUMENTS as d 
				where d.Id_URL in {} and dsc.url=d.url ORDER By dsc.Date ASC""".format(dataPost))
		else:
			cursor1.execute("""SELECT DISTINCT( dsc.`URL`), dsc.`Date`, dsc.`Share_Count`, d.Id_URL 
				FROM DOCUMENTS_SHAREDCOUNT_TREND_7_DIAS as dsc, DOCUMENTS as d 
				where d.Id_URL = {} and dsc.url=d.url ORDER By dsc.Date ASC""".format(dataPost))
		myresult = cursor1.fetchall()
		data = DataFrame(myresult,
  			columns=['URL', 'Date', 'Share_Count', 'Id_URL'])
		listData = []
		for row in data.iterrows():
			d = {}
			d['URL'] = row[1]["URL"]
			d['Date'] = row[1]["Date"].strftime('%Y-%m-%d %H:%M:%S')
			d['Share_Count'] = row[1]["Share_Count"]
			listData.append(d)
		dataResponse = {
			'status': "success",
			'code': 200,
			'data': listData,
			'message': 'null'
		}
		dataResponse = json.dumps(dataResponse)
		#print(dataResponse)
		return HttpResponse(dataResponse, content_type='application/json')



class ApiGetBGDocuments7AllByClient(View):
	def get(self, request):
		
		cnx = mysql.connector.connect(user='admin', password='3y3w4tch20204dm1n',
            host='meltwater-dbcluster-instance-1.cffatgb5exir.us-west-2.rds.amazonaws.com',
            database='meltwater')
		cursor1 = cnx.cursor(buffered=True)
		date_hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		date_ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

		cursor1.execute("""
			SELECT `Date`, 
			Headline, URL, Opening_Text, 
			Hit_Sentence, Source, Influencer, 
			Country, Subregion, `Language`, 
			Reach, Desktop_Reach, Mobile_Reach, 
			Twitter_Social_Echo, Facebook_Social_Echo, 
			Reddit_Social_Echo, Social_Echo, AVE, 
			Sentiment, Key_Phrases, Input_Name, 
			Keywords, Body, Tipo_informacion, 
			Pais_campaña, Cliente, Nombre_campaña, 
			Enlace, Estado, Imagen, Share_Count, Id_URL 
			FROM meltwater.DOCUMENTS_7_DIAS
			WHERE Cliente = '%s' AND Estado = 1 
			AND date BETWEEN '%s' AND '%s'
		""" % ('PC',date_ayer, date_hoy))
		myresult = cursor1.fetchall()
		data = DataFrame(myresult,
  			columns=['Date', 'Headline', 'URL', 'Opening_Text', 
  			'Hit_Sentence', 'Source', 'Influencer', 'Country', 
  			'Subregion', 'Language', 'Reach', 'Desktop_Reach', 
  			'Mobile_Reach', 'Twitter_Social_Echo', 
  			'Facebook_Social_Echo', 'Reddit_Social_Echo', 
  			'Social_Echo', 'AVE', 'Sentiment', 'Key_Phrases', 
  			'Input_Name', 'Keywords', 'Body', 
  			'Tipo_informacion', 'Pais_campaña', 
  			'Cliente', 'Nombre_campaña', 'Enlace', 
  			'Estado', 'Imagen', 'Share_Count', 'Id_URL'])
		listData = []
		for row in data.iterrows():
			d = {}
			d['Id_URL'] = row[1]["Id_URL"]
			d['Date'] = row[1]["Date"].strftime('%Y-%m-%d %H:%M:%S')
			d['Headline'] = row[1]["Headline"]
			d['Opening_Text'] = row[1]["Opening_Text"]
			d['Hit_Sentence'] = row[1]["Hit_Sentence"]
			d['Source'] = row[1]["Source"]
			d['Influencer'] = row[1]["Influencer"]
			d['Country'] = row[1]["Country"]
			d['Subregion'] = row[1]["Subregion"]
			d['Language'] = row[1]["Language"]
			d['Reach'] = row[1]["Reach"]
			d['Desktop_Reach'] = row[1]["Desktop_Reach"]
			d['Mobile_Reach'] = row[1]["Mobile_Reach"]
			d['Twitter_Social_Echo'] = row[1]["Twitter_Social_Echo"]
			d['Facebook_Social_Echo'] = row[1]["Facebook_Social_Echo"]
			d['Reddit_Social_Echo'] = row[1]["Reddit_Social_Echo"]
			d['Social_Echo'] = row[1]["Social_Echo"]
			d['AVE'] = row[1]["AVE"]
			d['Sentiment'] = row[1]["Sentiment"]
			d['Key_Phrases'] = row[1]["Key_Phrases"]
			d['Input_Name'] = row[1]["Input_Name"]
			d['Keywords'] = row[1]["Keywords"]
			d['Body'] = row[1]["Body"]
			d['Tipo_informacion'] = row[1]["Tipo_informacion"]
			d['Pais_campaña'] = row[1]["Pais_campaña"]
			d['Cliente'] = row[1]["Cliente"]
			d['Nombre_campaña'] = row[1]["Nombre_campaña"]
			d['Enlace'] = row[1]["Enlace"]
			d['Estado'] = row[1]["Estado"]
			d['Imagen'] = row[1]["Imagen"]
			d['Share_Count'] = row[1]["Share_Count"]
			d['Id_URL'] = row[1]["Id_URL"]
			d['URL'] = row[1]["URL"]
			if (row[1]["Keywords"] in row[1]["Headline"]) or (row[1]["Keywords"] in row[1]["Hit_Sentence"]) or (row[1]["Keywords"] in row[1]["Opening_Text"]):
				d["Primaria"] = "true"
			else: d["Primaria"] = "false"
			
			d['Share_Count'] = row[1]["Share_Count"]
			listData.append(d)


		dataResponse = {
			'status': "success",
			'code': 200,
			'data': listData,
			'message': 'null'
		}
		dataResponse = json.dumps(dataResponse)
		#print(dataResponse)
		return HttpResponse(dataResponse, content_type='application/json')