from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

# def index(request):
#     return HttpResponse("<h1> Hello world !</h1>")
def index(response):
    return render(response, "main/index.html")

def info(response):
    return render(response, "main/info.html")