import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
from ..models import Resumen,ResumenFiltros,ResumenProductosUsuario,ResumenInfoPersonaNatural,ResumenFinancieraMe,Cliente,ResumenInfoPersonaJuridica
from django.template import loader
from rest_framework.exceptions import ValidationError, NotFound
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.db.models import Sum,Count
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators  import  permission_required

def index(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/consdavivienda/accounts/login/')
	latest_question_list = Resumen.objects
	template = loader.get_template('consdavivienda/index.html')
	context = {
		'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))
		
def elementos_id(request, id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/consdavivienda/accounts/login/')
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
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/consdavivienda/accounts/login/')
		
	try:
		clienteObj = Cliente.objects.get(identificacion=id)
		if clienteObj.tipo_persona == 'PN' : 
			resumenInfoPersona=ResumenInfoPersonaNatural.objects.get(identificacion=id)
		else :
			resumenInfoPersona=ResumenInfoPersonaJuridica.objects.get(identificacion=id)	
		
		productosResult = ResumenProductosUsuario.objects.filter(identificacion=id)
		
		try :
			resumenInfoFinancieraMe =  ResumenFinancieraMe.objects.get(identificacion=id)
		except :
		    resumenInfoFinancieraMe="";
		
		if clienteObj.tipo_persona == 'PN' : 
			return render(request, 'consdavivienda/tarjetaresumen_pnatural.html', {'resumenObject': resumenInfoPersona,'productosResult':productosResult,'resumenInfoFinancieraMe':resumenInfoFinancieraMe})
		else:
			return render(request, 'consdavivienda/tarjetaresumen_pjuridica.html', {'resumenObject': resumenInfoPersona,'productosResult':productosResult,'resumenInfoFinancieraMe':resumenInfoFinancieraMe})
	except Cliente.DoesNotExist:
		return render(request, 'consdavivienda/NoFound.html', {'error':'No existe id'})		
	except 	ResumenInfoPersonaNatural.DoesNotExist:
		return render(request, 'consdavivienda/NoFound.html', {'error':'No existe id'})	
	except 	ResumenInfoPersonaJuridica.DoesNotExist:
		return render(request, 'consdavivienda/NoFound.html', {'error':'No existe id'})	
	"""	
	except 	productosResult.DoesNotExist:
		return render(request, 'consdavivienda/NoFound.html', {'error':'No existe id'})
	except 	productosResult.DoesNotExist:
		return render(request, 'consdavivienda/NoFound.html', {'error':'No existe id'})
	"""	
	
def chartsresumen(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/consdavivienda/accounts/login/')
		
	latest_question_list = Resumen.objects
	template = loader.get_template('consdavivienda/chartsresumen.html')
	context = {
		'latest_question_list': latest_question_list,
	}
	return HttpResponse(template.render(context, request))


def total_divisas(request,id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/consdavivienda/accounts/login/')
		
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
		
# Create your views here.
def sugiereIdentificacion(request,id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/consdavivienda/accounts/login/')
	try:
		elementos = ResumenFiltros.objects.raw('SELECT id,identificacion, descripcion as nombre , tipo_persona as primer_apellido FROM consdavivienda_cliente WHERE identificacion like %s LIMIT 10',[id+'%'])
	except:
		raise ValidationError({'id': ['No existe elementos ' + id]})
	data = serializers.serialize('json',elementos)	
	return HttpResponse(data, content_type='application/json')
	
def layout1(request):	
	try:
		resumenInfoPersonaNatural =  ResumenInfoPersonaNatural.objects.get(identificacion=19163522)
		productosResult = ResumenProductosUsuario.objects.filter(identificacion=19163522)
		resumenInfoFinancieraMe =  ResumenFinancieraMe.objects.get(identificacion=19163522)
	except resumenInfoPersonaNatural.DoesNotExist:
		return render(request, 'consdavivienda/NoFound.html', {'error':'No existe id'})
	return render(request, 'consdavivienda/tarjetaresumen_pnatural.html', {'resumenObject': resumenInfoPersonaNatural,'productosResult':productosResult,'resumenInfoFinancieraMe':resumenInfoFinancieraMe})

