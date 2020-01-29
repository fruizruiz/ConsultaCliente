from django.test import TestCase
from django.urls import path
from . import views
from rest_framework import routers
from consdavivienda import views
from django.conf.urls import url,include
from .views import ResumenDatail,error_404_view
from django.conf.urls import handler404,handler400,handler500 


# Create your tests here.
app_name = 'consdavivienda'
urlpatterns = [
	path('', views.index, name='home'), 
	url(r'^tarjetaresumen/(?P<id>\d+)/$', views.tarjetaresumen, name='tarjetaresumen'),
	url(r'^elementos/(?P<id>\d+)/$', views.elementos_id, name='elementoId'),
	url(r'^chartsresumen/$', views.chartsresumen, name='chartsresumen'),
	url(r'^totaldivisas/(?P<id>\d+)/$', views.total_divisas,name='elementoId'),
    path('consultaresumen/<int:pk>/', views.ResumenDatail.as_view()),
	path('accounts/', include('django.contrib.auth.urls')),
	url(r'^sugiereIdentificacion/(?P<id>\d+)/$', views.sugiereIdentificacion, name='sugiereIdentificacion'),
	url(r'^layout1/$', views.layout1, name='layout1'),
]
handler404 = 'consdavivienda.views.error_404_view'
handler400 = 'consdavivienda.views.error_400_view'
