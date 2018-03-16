"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework.authtoken import views as drf_views
from django.contrib.auth.decorators import login_required
from . import views
from nps.views import survey_data, SurveyViewset, client_data, product_data, products, user_types, client_deltas
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'surveys', SurveyViewset)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    url(r'^auth/', drf_views.obtain_auth_token, name='auth'),
    url(r'^dashboard/', login_required(views.ReactAppView.as_view(), login_url='/admin/login')),
    url(r'^survey/', survey_data),
    url(r'^client_data/', client_data),
    url(r'^product_data/', product_data),
    url(r'^products/', products),
    url(r'^user_types/', user_types),
    url(r'^client_deltas/', client_deltas),
    url(r'^', include(router.urls)),

]
