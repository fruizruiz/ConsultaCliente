from django.shortcuts import render
from django.http import HttpResponse

def error_404_view(request, exception):
    data = {""}
    return render(request,'consdavivienda/404.html', data)
	
def error_400_view(request, exception):
    data = {""}
    return render(request,'consdavivienda/404.html', data)
