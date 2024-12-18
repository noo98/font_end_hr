from django.shortcuts import render
# Create your views here.
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def fetch_items(request):
    backend_url = "http://192.168.45.49:8001//api/items/"
    response = requests.get(backend_url)
    return Response(response.json())
def index(request):
    return render(request, 'index.html',)

def tables_emp(request):
    api_url = "http://192.168.45.71:8000/api/list/employees/"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        context = {'employees': data}
    else:
        context = {'employees': []}

    return render(request, 'tables_emp.html', context=context)

def form_emp(request):
    return render(request, 'form_emp.html',)

def form_post(request):
    return render(request, 'form_post.html',)

def post(request):
    return render(request, 'post.html',)

def test(request):
    return render(request, 'test.html',)

# import requests
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# @api_view(['GET'])
# def fetch_items(request):
#     backend_url = "http://192.168.45.49:8001/api/items/"
#     response = requests.get(backend_url)
#     return Response(response.json())