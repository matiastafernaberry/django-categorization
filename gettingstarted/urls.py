from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

import hello.views
from hello.views import *


# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
	path("", csrf_exempt(MainClass.as_view())),
    path("keywordextract/", csrf_exempt(NameExtractClass.as_view())),
    path("nameextract/", csrf_exempt(NameExtractClass.as_view())),
    path("buzztracker/", csrf_exempt(BuzzTrackerClass.as_view())),
    path("buzztrackerjson/", csrf_exempt(BuzzTrackerJsonClass.as_view())),
    path("rake/", csrf_exempt(RakeTest.as_view())),
    path("admin/", admin.site.urls),
]
