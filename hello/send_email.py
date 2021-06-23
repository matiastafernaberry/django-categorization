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
import smtplib
import datetime
from email.message import EmailMessage

from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View



class SendEmailClass(View):
	@csrf_exempt
	def post(self, request):
		dataPost = request.body.decode('utf-8')
		dataPost = json.loads(dataPost)
		print(dataPost)
		hora = datetime.datetime.now()
		hora = hora.strftime("%d-%m-%Y, %H:%M:%S")
		content = '<table>'
		content += "<tr><td style='padding:10px;font-weight:700;'>Desde: beenews.hellobee.io</td></tr>"
		content += "<tr><td style='padding:10px;font-weight:700;'>Nombre: {0}</td></tr>".format(dataPost['nombre'])
		content += "<tr><td style='padding:10px;font-weight:700;'>Apellido: {0}</td></tr>".format(dataPost['apellido'])
		content += "<tr><td style='padding:10px;font-weight:700;'>Correo Electronico: {0}</td></tr>".format(dataPost['email'])
		content += "<tr><td style='padding:10px;font-weight:700;'>Numero de telefono movil:	{0}</td>".format(dataPost['telefono'])
		content += "<tr><td style='padding:10px;font-weight:700;'>Empresa: {0}</td></tr>".format(dataPost['nombre_empresa'])
		content += "<tr><td style='padding:10px;font-weight:700;'>Direccion web empresa: {0}</td></tr>".format(dataPost['direccion_empresa'])
		content += "<tr><td style='padding:10px;font-weight:700;'>Datos usuario: {0}</td></tr>".format(dataPost['datoUser'])
		content += "<tr><td style='padding:10px;font-weight:700;'>Hora: {0}</td></tr></table>".format(hora)

		msg = EmailMessage()
		msg['Subject'] = 'Solicitud de demo de BeeNews'
		# msg['From'] = "beenews.hellobee.io"
		msg['To'] = "ask@hellobee.io"
		msg.add_header('Content-Type','text/html')
		msg.set_payload(content)
		# Send the message via our own SMTP server.
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
		server.login("beenews.hellobee@gmail.com", "p1x4bl3s0ft4ws!")
		server.send_message(msg)
		server.quit()

		obj = {'data': 'email send ok'}
		dump = json.dumps(obj)
		return HttpResponse(dump, content_type='application/json')