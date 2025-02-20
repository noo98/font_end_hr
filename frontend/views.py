from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
import json
from django.http import JsonResponse
import environ
import os


env = environ.Env()
environ.Env.read_env()  
DATABASE_URL = env('DATABASE_URL')  




@api_view(['GET'])

def index(request):
    return render(request, 'index.html')
def index1(request):
    return render(request, 'index1.html')

def tables_emp(request):
    api_url = f"{DATABASE_URL}/api/employee/"
    departments_api = f"{DATABASE_URL}/api/list/departments/"

    employees = []

    try:
        emp_response = requests.get(api_url)
        dept_response = requests.get(departments_api)

        if emp_response.status_code == 200:
            emp_data = emp_response.json()
        else:
            emp_data = []

        if dept_response.status_code == 200:
            dept_data = dept_response.json()
        else:
            dept_data = []

        department_map = {dept["id"]: dept["name"] for dept in dept_data}

        for emp in emp_data:
            employees.append({
                "emp_id": emp.get("emp_id", "N/A"),
                "lao_name": emp.get("lao_name", "N/A"),
                "eng_name": emp.get("eng_name", "N/A"),
                "nickname": emp.get("nickname", "N/A"),
                "Gender": emp.get("Gender", "N/A"),
                "department": department_map.get(emp.get("department"), "N/A"),
            })
    
    except Exception as e:
        print(" Error fetching data:", e)

    return render(request, 'tables_emp.html', {"employees": employees})

def doc_format(request):
    url = "http://192.168.45.71:8000/api/list/Document_format/"
    
    # Fetch data from the API
    try:
        response = requests.get(url)
        response.raise_for_status()  
        doc_format = response.json()  
        # print(documents)  
    except requests.exceptions.RequestException as e:
        doc_format = []  
        print(f"Error fetching data: {e}")
     
    return render(request, 'doc_format.html', {'doc_format': doc_format})

def department(request):
    url = "http://192.168.45.71:8000/api/list/departments/"
    
    # Fetch data from the API
    try:
        response = requests.get(url)
        response.raise_for_status()  
        department = response.json()  
        # print(documents)  
    except requests.exceptions.RequestException as e:
        department = []  
        print(f"Error fetching data: {e}")   
    return render(request, 'department.html', {'department': department})

def register(request):
    # API URLs
    users_api = "http://192.168.45.71:8000/api/users"
    departments_api = "http://192.168.45.71:8000/api/list/departments/"
    employees_api = "http://192.168.45.71:8000/api/employee"

    try:
        users = requests.get(users_api).json()  # ດຶງຂໍ້ມູນ user
        departments = requests.get(departments_api).json()  # ດຶງຂໍ້ມູນ department
        employees = requests.get(employees_api).json()  # ດຶງຂໍ້ມູນ employee

        # ສ້າງແຜນທີ່ຂອງ department
        department_map = {dept["id"]: dept["name"] for dept in departments}
        
        # ສ້າງແຜນທີ່ຂອງ employee
        employee_map = {emp["emp_id"]: emp["lao_name"] for emp in employees}

        # ສະຖານະຂອງ User
        status_map = {
            1: "Admin",
            2: "User MM",
            3: "User IT",
            4: "User OP",
            5: "User DQ",
        }

        # ປະກອບຂໍ້ມູນໃຫ້ພ້ອມສົ່ງໄປໃນ template
        register_list = []
        for user in users:
            register_list.append({
                "id": user["us_id"],
                "username": user["username"],
                "employee_name": employee_map.get(user["Employee"], "N/A"),
                "department_name": department_map.get(user["Department"], "N/A"),
                "status": status_map.get(user["status"], "Unknown")  # ດຶງສະຖານະຕາມຄ່າ
            })

    except Exception as e:
        register_list = []
        print("Error fetching data:", e)

    return render(request, 'register.html', {"register": register_list})

def education_level(request):
    return render(request, 'education_level.html',)

def salary_grade(request):
    return render(request, 'salary_grade.html',)

def profile(request):
    return render(request, 'profile.html',)

def form_login(request):
    return render(request, "form_login.html")

DATABASE_URL = os.getenv('DATABASE_URL')
def documentEntry(request):
    department_into = request.GET.get('department_into', '')
    # print(f"department_into: {department_into}")
    
    document_api_url = f'http://192.168.45.71:8000/api/search/document_lcic/?doc_type_info=ຂາເຂົ້າ&department_into={department_into}'
    # print(f"document_api_url: {document_api_url}")
    department_api_url = "http://192.168.45.71:8000/api/list/departments/"
    format_api_url = "http://192.168.45.71:8000/api/list/Document_format/"
    
    
    format_filter = request.GET.get('format', '')
    department_filter = request.GET.get('department', '')
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')
    
    try:
        # Fetch departments (cached)
        departments = cache.get('departments')
        if not departments:
            response = requests.get(department_api_url)
            departments = response.json() if response.status_code == 200 else []
            cache.set('departments', departments, timeout=60 * 15)
        
        # Fetch formats (cached)
        formats = cache.get('formats')
        if not formats:
            response = requests.get(format_api_url)
            formats = response.json() if response.status_code == 200 else []
            cache.set('formats', formats, timeout=60 * 15)
        
        # Fetch documents
        response = requests.get(document_api_url)
        response.raise_for_status()
        documents = response.json()
        
        # Map department and format names
        department_map = {str(d['id']): d['name'] for d in departments}
        format_map = {str(f['dmf_id']): f['name'] for f in formats}
        
        for doc in documents:
            doc['department'] = department_map.get(str(doc.get('department', {}).get('id', '')), 'N/A')
            doc['format_name'] = format_map.get(str(doc.get('format', {}).get('dmf_id', '')), 'N/A')
            
            if isinstance(doc.get('department_into'), list):
                doc['department_into'] = [department_map.get(str(dep.get('id', '')), 'N/A') for dep in doc['department_into']]
            else:
                doc['department_into'] = []
        
        # Apply filters
        if format_filter:
            documents = [doc for doc in documents if str(doc.get('format', {}).get('dmf_id', '')) == format_filter]
        if department_filter:
            department_name_filter = department_map.get(department_filter, 'N/A')
            documents = [doc for doc in documents if doc['department'] == department_name_filter]
        if start_date_filter:
            documents = [doc for doc in documents if doc.get('insert_date', '') >= start_date_filter]
        if end_date_filter:
            documents = [doc for doc in documents if doc.get('insert_date', '') <= end_date_filter]
    
    except requests.exceptions.RequestException as e:
        documents = []
        print(f"Error fetching API data: {e}")
    
    return render(request, 'documentEntry.html', 
                  {
        'department_into': department_into,
        'documents': documents,
        'departments': departments,
        'formats': formats,
        'format_filter': format_filter,
        'department_filter': department_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
        'documents_json': json.dumps(documents),
    }
    )

# def documentEntry(request):
#     department_into = request.GET.get('department_into', '')
    
#     document_api_url =  f'http://192.168.45.71:8000/api/search/document_lcic/?doc_type_info=ຂາເຂົ້າ&department_into={department_into}'
#     department_api_url = "http://192.168.45.71:8000/api/list/departments/"
#     format_api_url = "http://192.168.45.71:8000/api/list/Document_format/"

#     format_filter = request.GET.get('format', '')
#     department_filter = request.GET.get('department', '')
#     start_date_filter = request.GET.get('start_date', '')
#     end_date_filter = request.GET.get('end_date', '')

#     try:
#         documents_response = requests.get(document_api_url)
#         departments_response = requests.get(department_api_url)
#         formats_response = requests.get(format_api_url)

#         documents = documents_response.json() if documents_response.status_code == 200 else []
#         departments = departments_response.json() if departments_response.status_code == 200 else []
#         formats = formats_response.json() if formats_response.status_code == 200 else []

#         department_map = {d['id']: d['name'] for d in departments}
#         format_map = {f['dmf_id']: f['name'] for f in formats}

#         for doc in documents:

#             doc['department'] = department_map.get(doc['department']['id'], 'N/A') if doc.get('department') else 'N/A'
            
#             doc['format_name'] = format_map.get(doc['format']['dmf_id'], 'N/A') if doc.get('format') else 'N/A'
            
#             if 'department_into' in doc and isinstance(doc['department_into'], list):
#                 doc['department_into'] = [department_map.get(dep['id'], 'N/A') for dep in doc['department_into']]
#             else:
#                 doc['department_into'] = []

#         if format_filter:
#             documents = [doc for doc in documents if str(doc['format']['dmf_id']) == format_filter]
#         if department_filter:
#             documents = [doc for doc in documents if str(doc['department']) == department_filter]
#         if start_date_filter:
#             documents = [doc for doc in documents if doc['insert_date'] >= start_date_filter]
#         if end_date_filter:
#             documents = [doc for doc in documents if doc['insert_date'] <= end_date_filter]

#     except requests.exceptions.RequestException as e:
#         documents = []
#         print(f"Error fetching API data: {e}")

#     return render(request, 'documentEntry.html', 
#                   {
#         'documents': documents,
#         'departments': departments,
#         'formats': formats,
#         'format_filter': format_filter,
#         'department_filter': department_filter,
#         'start_date_filter': start_date_filter,
#         'end_date_filter': end_date_filter,
#         'documents_json': json.dumps(documents),
#     }
#     )


def documentOut(request):

    document_api_url = "http://192.168.45.71:8000/api/list/document_lcic/"
    department_api_url = "http://192.168.45.71:8000/api/list/departments/"
    format_api_url = "http://192.168.45.71:8000/api/list/Document_format/"

    format_filter = request.GET.get('format', '')
    department_filter = request.GET.get('department', '')
    start_date_filter = request.GET.get('start_date', '')
    end_date_filter = request.GET.get('end_date', '')

    try:
        # ດຶງຂໍ້ມູນ API
        documents_response = requests.get(document_api_url)
        departments_response = requests.get(department_api_url)
        formats_response = requests.get(format_api_url)

        documents = documents_response.json() if documents_response.status_code == 200 else []
        departments = departments_response.json() if departments_response.status_code == 200 else []
        formats = formats_response.json() if formats_response.status_code == 200 else []

        # ສ້າງແຜນທີ່ (Mapping) ຂໍ້ມູນ
        department_map = {d['id']: d['name'] for d in departments}
        format_map = {f['dmf_id']: f['name'] for f in formats}

        # ປັບປຸງຂໍ້ມູນໃນ documents
        for doc in documents:
            # ແມບ department
            doc['department'] = department_map.get(doc['department']['id'], 'N/A') if doc.get('department') else 'N/A'
            
            # ແມບ format
            doc['format_name'] = format_map.get(doc['format']['dmf_id'], 'N/A') if doc.get('format') else 'N/A'
            
            # ແມບ department_into
            if 'department_into' in doc and isinstance(doc['department_into'], list):
                doc['department_into'] = [department_map.get(dep['id'], 'N/A') for dep in doc['department_into']]
            else:
                doc['department_into'] = []

        # ການຄັດຕອງ (Filtering)
        if format_filter:
            documents = [doc for doc in documents if str(doc['format']['dmf_id']) == format_filter]
        if department_filter:
            documents = [doc for doc in documents if str(doc['department']) == department_filter]
        if start_date_filter:
            documents = [doc for doc in documents if doc['insert_date'] >= start_date_filter]
        if end_date_filter:
            documents = [doc for doc in documents if doc['insert_date'] <= end_date_filter]

    except requests.exceptions.RequestException as e:
        documents = []
        print(f"Error fetching API data: {e}")

    return render(request, 'documentOut.html', {
        'documents': documents,
        'departments': departments,
        'formats': formats,
        'format_filter': format_filter,
        'department_filter': department_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
    })
def documentGen(request):
    return render(request, 'documentGen.html',)

def add_documentE(request):
    return render(request, 'add_document_entry.html',)

def add_documentO(request):
    return render(request, 'add_document_out.html',)

def add_documentG(request):
    return render(request, 'add_documentGeneral.html',)

def update_document(request, doc_id):
    document_url = f"http://192.168.45.71:8000/api/list/document_lcic/{doc_id}/"
    departments_url = "http://192.168.45.71:8000/api/list/departments/"
    document_format_url = "http://192.168.45.71:8000/api/list/Document_format/"
    update_url = f"http://192.168.45.71:8000/api/update/document_lcic/{doc_id}/"

    if request.method == 'GET':
        try:
            document = requests.get(document_url).json()
            departments = requests.get(departments_url).json()
            document_format = requests.get(document_format_url).json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            document, departments, document_format = {}, [], []
            
        return render(request, 'update_document.html', {
            'document': document,
            'departments': departments,
            'Document_format': document_format,
        })

    elif request.method == 'POST':        
        try:
            data = {
                'doc_number': request.POST.get('doc_number'),
                'insert_date': request.POST.get('insert_date'),
                'subject': request.POST.get('subject'),
                'format': request.POST.get('format'),
                'doc_type': request.POST.get('doc_type'),
                'document_detail': request.POST.get('document_detail'),
                'department': request.POST.get('department'),
                'name': request.POST.get('name'),
            }
            if request.FILES.get('file'):
                files = {'file': request.FILES['file']}
                response = requests.put(update_url, data=data, files=files)  
            else:
                response = requests.put(update_url, json=data)  
            
            response.raise_for_status()
            return JsonResponse({'success': True, 'message': 'ບັນທືກຂໍ້ມູນສຳເລັດ!'})
            
        except requests.exceptions.RequestException as e:
            print(f"Error updating document: {e}")
            return JsonResponse({'success': False, 'error': str(e)}, status=400)


            

def test_view(request):
    format_api_url = "http://192.168.45.71:8000/api/list/Document_format/"
    response = requests.get(format_api_url)

    formats = response.json() if response.status_code == 200 else []

    context = {
        'formats': formats,
        'format_filter': request.GET.get('format', '')
    }
    return render(request, "test.html", context)

def form_emp(request):
    return render(request, 'form_emp.html',)

def form_post(request):
    return render(request, 'form_post.html',)

def post(request):
    return render(request, 'post.html',)

def testttt(request):
    return render(request, 'testttt.html',)