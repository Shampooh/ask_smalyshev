"""Ask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from MalyshevAsk import views as ask_views

urlpatterns = [
    url(r'^vote/?', ask_views.vote),
    url(r'^correct/?', ask_views.correct),
    url(r'^logout/?', ask_views.logout, name = "logout"),
	url(r'^admin/?', admin.site.urls),
	url(r'^index/?', ask_views.index, name = "index"),
	url(r'^login/?', ask_views.login, name = "login"),
	url(r'^signup/?', ask_views.signup, name = "signup"),
	url(r'^personal_page/?', ask_views.personal_page, name = "personal_page"),
	url(r'^ask/?', ask_views.ask, name = "ask"),
    url(r'^question/(?P<qid>\d+)', ask_views.question, name = "question"),
    url(r'^searchByTag/?', ask_views.searchByTag, name = "tag"),
    url(r'^getPostParameters/?.*', ask_views.getPostParameters),
    url(r'^hot/?', ask_views.hot),
    url(r'^/?', ask_views.index, name = "index")
]