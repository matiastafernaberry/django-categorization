from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

import hello.views
import hello.byg
from hello.views import *
from hello.byg import *
from hello.send_email import *


# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
	#path("", csrf_exempt(MainClass.as_view())),
	path("", csrf_exempt(FileClass.as_view())),
    path("files/<str:filename>", csrf_exempt(FileDownloadClass.as_view())),
    path("bg-documents-sharedcount/", csrf_exempt(ApiGetDocumentsSharedCount7Class.as_view())),
    path("keywordextract/", csrf_exempt(NameExtractClass.as_view())),
    path("nameextract/", csrf_exempt(NameExtractClass.as_view())),
    path("buzztracker/", csrf_exempt(BuzzTrackerClass.as_view())),
    path("buzztrackerjson/", csrf_exempt(BuzzTrackerJsonClass.as_view())),
    path("buzztrackerjson/<int:file_id>/", csrf_exempt(BuzzTrackerJsonClass.as_view())),
    path("sendmail/", csrf_exempt(SendEmailClass.as_view())),
    path("unsubscribe/", csrf_exempt(SendEmailUnsubscribe.as_view())),
    path(".well-known/pki-validation/3B7A9D37194721F16B7EB9BDC026D751.txt", TemplateView.as_view(template_name='3055F8E464FD7CF2D51499F97436A2A3.txt',content_type='text/plain')),
    path("rake/", csrf_exempt(RakeTest.as_view())),
    path("admin/", admin.site.urls),
]
