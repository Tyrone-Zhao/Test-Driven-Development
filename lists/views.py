from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home_page(request):
    return HttpResponse("<html><title>待办事项清单</title></html>")
