#!/bin/bash
echo Starting django-categorization app.
cd /var/www/html/django-categorization/
gunicorn --bind ec2-52-38-13-82.us-west-2.compute.amazonaws.com:5000 gettingstarted.wsgi:application