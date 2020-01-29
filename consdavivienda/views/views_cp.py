import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from .models import Resumen
from django.template import loader
from rest_framework.exceptions import ValidationError, NotFound
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.db.models import Sum,Count
import json
from rest_framework import permissions

# Create your views here.

def index(request):
	latest_question_list = Resumen.objects
	template = loader.get_template('consdavivienda/index.html')
	context = {
		'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))

def elementos_id(request, id):
	if request.method == 'GET':
		try:
			elemento = Resumen.objects.get(identificacion=id)
		except:
			raise ValidationError({'id': ['No existe elemento ' + id]})
		return HttpResponse(serializers.serialize("json", [elemento]), content_type="application/json")
	else:
		raise NotFound(detail="No se encuentra comando rest elementos/{id} con metodo " + request.method)

# Create your views here.
def tarjetaresumen(request,id):
	try:
		resumen = Resumen.objects.get(identificacion=id)
	except Resumen.DoesNotExist:
		raise Http404("Resumen does not exist")
	return render(request, 'consdavivienda/tarjetaresumen.html', {'resumenObject': resumen})

def chartsresumen(request):
	latest_question_list = Resumen.objects
	template = loader.get_template('consdavivienda/chartsresumen.html')
	context = {
		'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))


def total_divisas(request,id):
	if request.method == 'GET':
		try:
			total_usd = Resumen.objects.all().aggregate(total_usd=Sum("total_tran_usd"))
			total_eur = Resumen.objects.all().aggregate(total_eur=Sum("total_tran_eur"))
			total_cad = Resumen.objects.all().aggregate(total_cad=Sum("total_tran_cad"))
			result ={'total_usd':total_usd['total_usd'],'total_eur':total_eur['total_eur'],'total_cad':total_cad['total_cad']}
		except:
			raise ValidationError({'id': ['No existe elemento ' + id]})
		return HttpResponse(json.dumps(result), content_type="application/json")
	else:
		raise NotFound(detail="No se encuentra comando rest elementos/{id} con metodo " + request.method)

