from django.shortcuts import render
# Create your views here.
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.http import JsonResponse




@api_view(['GET'])
def fetch_items(request):
    data = {"message": "Hello from fetch_items"}
    return JsonResponse(data)

def index(request):
    return render(request, 'index.html',)

# def tables_emp(request):
#     return render(request, 'tables_emp.html',)
def tables_emp(request):
    api_url = "http://192.168.45.71:8000/api/list/employees/"
    response = requests.get(api_url)

    if response.status_code == 200:
        employees = response.json()
    else:
        employees = []  # ສຳລັບກໍລະນີໂຫລດບໍ່ໄດ້
    return render(request, 'tables_emp.html', {'employees': employees})

def form_emp(request):
    return render(request, 'form_emp.html',)

def form_post(request):
    return render(request, 'form_post.html',)

def post(request):
    return render(request, 'post.html',)

def test(request):
    return render(request, 'test.html',)

def department(request):
    return render(request, 'department.html',)

def education_level(request):
    return render(request, 'education_level.html',)

def salary_grade(request):
    return render(request, 'salary_grade.html',)

def documents(request):
    # ລິ້ງ API
    api_url = "http://192.168.45.71:8000/api/list/DocumentEntry/"
    
    # ສົ່ງຄຳຂໍ້
    response = requests.get(api_url)
    
    if response.status_code == 200:
        documents = response.json()  # ດຶງຂໍ້ມູນທີ່ເປັນ JSON
    else:
        documents = {"error": "ບໍ່ສາມາດໂຫລດຂໍ້ມູນໄດ້"}
    
    # ສົ່ງຂໍ້ມູນໄປທີ່ template
    return render(request, 'documents.html', {'documents': documents})
