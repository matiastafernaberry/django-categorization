from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin
from django.views.generic import TemplateView


admin.autodiscover()

import hello.views
from hello.views import MainClass

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
	path("", TemplateView.as_view(template_name="index.html")),
    path("keywordextract/", csrf_exempt(MainClass.as_view())),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
]
