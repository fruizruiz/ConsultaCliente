import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.http import HttpResponse
from ..models import Resumen
from django.template import loader
from rest_framework.exceptions import ValidationError, NotFound
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.db.models import Sum,Count
import json
from rest_framework import permissions
from rest_framework.views import APIView
from ..serializers import ResumenSerializer
from rest_framework.response import Response
from ..permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

class ResumenDatail(APIView):
	#permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                  IsOwnerOrReadOnly]
	
	permission_classes = [IsAuthenticated,]

	def get_object(self, pk):
		try:
			return Resumen.objects.get(identificacion=pk)
		except Resumen.DoesNotExist:
			raise Http404
	
	def get(self, request, pk, format=None):
		resumen = self.get_object(pk)
		serializer = ResumenSerializer(resumen)
		return Response(serializer.data)