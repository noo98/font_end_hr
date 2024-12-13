from django.shortcuts import render

# Create your views here.
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def fetch_items(request):
    backend_url = "http://192.168.45.49:8001/api/items/"
    response = requests.get(backend_url)
    return Response(response.json())