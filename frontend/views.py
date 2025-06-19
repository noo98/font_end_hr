from django.shortcuts import render
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.cache import cache
import json
from django.http import JsonResponse
import environ
import os
from datetime import datetime

env = environ.Env()
environ.Env.read_env()  
DATABASE_URL = env('DATABASE_URL')  


@api_view(['GET'])

def index(request):
    return render(request, 'index.html',{ 'database_url': DATABASE_URL, })
def index1(request):
    return render(request, 'index1.html',{ 'database_url': DATABASE_URL, })

def tables_emp(request): 
    api_url = f"{DATABASE_URL}/api/employee/"
    departments_api = f"{DATABASE_URL}/api/list/departments/"
    positions_api = f"{DATABASE_URL}/api/positions/"
    
    employees = []

    try:
        # Fetch data from API
        emp_response = requests.get(api_url)
        dept_response = requests.get(departments_api)
        pos_response = requests.get(positions_api)
        # Check API response status
        emp_data = emp_response.json() if emp_response.status_code == 200 else []
        dept_data = dept_response.json() if dept_response.status_code == 200 else []
        pos_data = pos_response.json() if pos_response.status_code == 200 else []
        # Create department mapping
        department_map = {dept["id"]: dept["name"] for dept in dept_data}
        # print(f"API URL6: {department_map}")
        # Create position mapping
        position_map = {pos["pos_id"]: pos["name"] for pos in pos_data}
        # print(f"API URL7: {position_map}")
        # Process employee data
        for emp in emp_data:
            employees.append({
                "emp_id": emp.get("employee", {}).get("emp_id", "N/A"),
                "lao_name": emp.get("employee", {}).get("lao_name", "N/A"),
                "eng_name": emp.get("employee", {}).get("eng_name", "N/A"),
                "nickname": emp.get("employee", {}).get("nickname", "N/A"),
                "Gender": emp.get("employee", {}).get("Gender", "N/A"),
                "Department": department_map.get(emp.get("employee", {}).get("Department"), "N/A"),
                "position": position_map.get(emp.get("employee", {}).get("position"), "N/A"),
                "phone": emp.get("employee", {}).get("phone", "N/A"),
                "salary_level": emp.get("employee", {}).get("salary_level", "N/A"),

                # Additional Data
                "education": emp.get("education", []),
                "specialized_education": emp.get("specialized_education", []),
                "political_theory_education": emp.get("political_theory_education", []),
                "foreign_languages": emp.get("foreign_languages", []),
                "work_experiences": emp.get("work_experiences", []),
                "training_courses": emp.get("training_courses", []),
                "awards": emp.get("awards", []),
                "disciplinary_actions": emp.get("disciplinary_actions", []),
                "family_members": emp.get("family_members", []),
                "evaluation": emp.get("evaluation", {}),
            })

    except Exception as e:
        print(f"Error fetching data: {e}")
        employees = []  # Ensure employees is empty on error
        print("Employees:", employees)
    return render(request, 'employee/tables_emp.html', {
        "employees": employees,
        "database_url": DATABASE_URL,
    })
def print_emp(request, emp_id):
    base_url = f"{DATABASE_URL}/api/employee/{emp_id}/"
    departments_url = f"{DATABASE_URL}/api/list/departments/"
    positions_url = f"{DATABASE_URL}/api/positions/"

    if request.method == 'GET':
        data = {
            'employee': {},
            'personal_information': [],
            'education': [],
            'specialized_education': [],
            'political_theory_education': [],
            'foreign_languages': [],
            'work_experiences': [],
            'training_courses': [],
            'awards': [],
            'disciplinary_actions': [],
            'family_members': [],
            'evaluation': {},
        }
        departments = []
        positions = []

        try:
            response = requests.get(base_url)
            response.raise_for_status()
            employee_data = response.json()
            if not employee_data or not isinstance(employee_data, list):
                # logger.error("Invalid employee data format for ID %s", emp_id)
                data['error'] = "Invalid employee data format."
            else:
                employee_data = employee_data[0]  # Assuming data is a list
                # logger.debug("Fetched employee data for ID %s: %s", emp_id, employee_data)

                data['employee'] = employee_data.get('employee', {})
                data['personal_information'] = employee_data.get('personal_information', [])
                data['education'] = employee_data.get('education', [])
                data['specialized_education'] = employee_data.get('specialized_education', [])
                data['political_theory_education'] = employee_data.get('political_theory_education', [])
                data['foreign_languages'] = employee_data.get('foreign_languages', [])
                data['work_experiences'] = employee_data.get('work_experiences', [])
                data['training_courses'] = employee_data.get('training_courses', [])
                data['awards'] = employee_data.get('awards', [])
                data['disciplinary_actions'] = employee_data.get('disciplinary_actions', [])
                data['family_members'] = employee_data.get('family_members', [])
                data['evaluation'] = employee_data.get('evaluation', {})

        except requests.exceptions.RequestException as e:
            # logger.error("Error fetching employee data for ID %s: %s", emp_id, str(e))
            data['error'] = "Failed to fetch employee data."

        try:
            response = requests.get(departments_url)
            response.raise_for_status()
            departments = response.json()
            # logger.debug("Fetched departments: %s", departments)
        except requests.exceptions.RequestException as e:
            # logger.error("Error fetching departments: %s", str(e))
            departments = []
        try:
            response = requests.get(positions_url)
            response.raise_for_status()
            positions = response.json()
            # logger.debug("Fetched positions: %s", positions)
        except requests.exceptions.RequestException as e:
            # logger.error("Error fetching positions: %s", str(e))
            positions = []

        return render(request, 'employee/print_emp.html', {
            **data,
            'positions': positions,
            'departments': departments,
            'database_url': DATABASE_URL,
            'emp_id': emp_id,
        })


def doc_format(request):
    return render(request, 'doc_format.html', {'database_url': DATABASE_URL})

def department(request):
    url = f"{DATABASE_URL}/api/list/departments/"
    
    # Fetch data from the API
    try:
        response = requests.get(url)
        response.raise_for_status()  
        department = response.json()  
        # print(documents)  
    except requests.exceptions.RequestException as e:
        department = []  
        print(f"Error fetching data: {e}")   
    return render(request, 'department.html', {
        'department': department,                        
        'database_url': DATABASE_URL,  
    })

def register(request):
    users_api = f"{DATABASE_URL}/api/users/"
    departments_api = f"{DATABASE_URL}/api/list/departments/"
    employees_api = f"{DATABASE_URL}/api/employee/"

    try:
        users_response = requests.get(users_api)
        if users_response.status_code != 200:
            raise Exception(f"Users API returned {users_response.status_code}: {users_response.text}")
        users = users_response.json()
        # print("Users:", users)

        departments_response = requests.get(departments_api)
        if departments_response.status_code != 200:
            raise Exception(f"Departments API returned {departments_response.status_code}: {departments_response.text}")
        departments = departments_response.json()
        # print("Departments:", departments)

        employees_response = requests.get(employees_api)
        if employees_response.status_code != 200:
            raise Exception(f"Employees API returned {employees_response.status_code}: {employees_response.text}")
        employees = employees_response.json()
        # print("Employees:", employees)

        # ປັບໃຫ້ເຂົ້າເຖິງ "employee" ພາຍໃນ JSON
        department_map = {dept["id"]: dept["name"] for dept in departments}
        employee_map = {emp["employee"]["emp_id"]: emp["employee"]["lao_name"] for emp in employees}

        status_map = {1: "Admin", 2: "User MM", 3: "User IT", 4: "User OP", 5: "User DQ"}

        register_list = []
        for user in users:
            register_list.append({
                "id": user["us_id"],
                "username": user["username"],
                "employee_name": employee_map.get(user["Employee"], "N/A"),
                "department_name": department_map.get(user["Department"], "N/A"),
                "status": status_map.get(user["status"], "Unknown"),
                "pic": user["pic"] if user["pic"] else ""
            })
        # print("Register List:", register_list)

    except Exception as e:
        register_list = []
        print("Error fetching data:", str(e))

    return render(request, 'register.html', {
        "register": register_list,
        'database_url': DATABASE_URL,
    })
        
def position(request):
    url = f"{DATABASE_URL}/api/positions/"
    # print(f"document_api_url: {url}")
    # Fetch data from the API
    try:
        response = requests.get(url)
        response.raise_for_status()  
        positions = response.json()  
        print("Positions:", positions)  
    except requests.exceptions.RequestException as e:
        positions = []  
        # print(f"Error fetching data: {e}")   
    return render(request, 'position.html', {
        'positions': positions,                        
        'database_url': DATABASE_URL,  
    })

def salary_grade(request):
    return render(request, 'salary_grade.html',)

def profile(request):
    return render(request, 'profile.html',)

def form_login(request):
    return render(request, "form_login.html",{
        'database_url': DATABASE_URL,  
    })

DATABASE_URL = os.getenv('DATABASE_URL')
def documentEntry(request):
    department_into = request.GET.get('department_into', '')
    # print(f"department_into: {department_into}")
    
    document_api_url = f'{DATABASE_URL}/api/search/document_lcic/?doc_type_info=ຂາເຂົ້າ&department_into={department_into}'
    # print(f"document_api_url: {document_api_url}")
    department_api_url = f"{DATABASE_URL}/api/list/departments/"
    format_api_url = f"{DATABASE_URL}/api/list/Document_format/"
    
    
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
            doc['format_name'] = format_map.get(doc['format']['dmf_id'], 'N/A') if doc.get('format') else 'N/A'
            
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
    
    return render(request, 'documents/documentEntry.html', 
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
        'database_url': DATABASE_URL,
    })



def documentOut(request):
    document_api_url = f"{DATABASE_URL}/api/list/document_lcic/"
    department_api_url = f"{DATABASE_URL}/api/list/departments/"
    format_api_url = f"{DATABASE_URL}/api/list/Document_format/"

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
            doc['department'] = department_map.get(doc['department']['id'], 'N/A') if doc.get('department') else 'N/A'
            doc['format_name'] = format_map.get(doc['format']['dmf_id'], 'N/A') if doc.get('format') else 'N/A'
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

    return render(request, 'documents/documentOut.html', {
        'documents': documents,
        'departments': departments,
        'formats': formats,
        'format_filter': format_filter,
        'department_filter': department_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
        'documents_json': json.dumps(documents),
        'database_url': DATABASE_URL,  
    })
def view_post(request):
    return render(request, 'documents/view_post.html', {       
        'database_url': DATABASE_URL,  
    })
def documentGen(request):
    document_api_url = f"{DATABASE_URL}/api/document_general/"
    department_api_url = f"{DATABASE_URL}/api/list/departments/"
    format_api_url = f"{DATABASE_URL}/api/list/Document_format/"

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


    except requests.exceptions.RequestException as e:
        documents = []
        print(f"Error fetching API data: {e}")

    return render(request, 'documents/documentGen.html', {
        'documents': documents,
        'departments': departments,
        'formats': formats,
        'format_filter': format_filter,
        'department_filter': department_filter,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
        'database_url': DATABASE_URL,  
    })

def add_documentE(request):
    return render(request, 'documents/add_document_entry.html',{
        'database_url': DATABASE_URL,  
    })

def add_documentO(request):
    return render(request, 'documents/add_document_out.html',{               
        'database_url': DATABASE_URL,  
    })

def add_documentG(request):   
    return render(request, 'documents/add_documentGeneral.html',{            
        'database_url': DATABASE_URL, 
    })

def update_documentE(request, doc_id):
    document_url = f"{DATABASE_URL}/api/list/document_lcic/{doc_id}/"
    departments_url = f"{DATABASE_URL}/api/list/departments/"
    document_format_url = f"{DATABASE_URL}/api/list/Document_format/"

    if request.method == 'GET':
        try:
            document = requests.get(document_url).json()
            departments = requests.get(departments_url).json()
            document_format = requests.get(document_format_url).json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            document, departments, document_format = {}, [], []

        return render(request, 'documents/update_documentE.html', {
            'document': document,
            'departments': departments,
            'Document_format': document_format,
            'database_url': DATABASE_URL,  
            'doc_id': doc_id,  
        })

    # ບໍ່ຈັດການ POST ທີ່ນີ້ ເພາະ frontend ຈະເຮັດແທນ
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

def update_documentO(request, doc_id):
    document_url = f"{DATABASE_URL}/api/list/document_lcic/{doc_id}/"
    departments_url = f"{DATABASE_URL}/api/list/departments/"
    document_format_url = f"{DATABASE_URL}/api/list/Document_format/"

    if request.method == 'GET':
        try:
            document = requests.get(document_url).json()
            departments = requests.get(departments_url).json()
            document_format = requests.get(document_format_url).json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            document, departments, document_format = {}, [], []

        return render(request, 'documents/update_documentO.html', {
            'document': document,
            'departments': departments,
            'Document_format': document_format,
            'database_url': DATABASE_URL,  
            'doc_id': doc_id,  
        })

    # ບໍ່ຈັດການ POST ທີ່ນີ້ ເພາະ frontend ຈະເຮັດແທນ
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

        
def update_documentGen(request, docg_id):
    document_url = f"{DATABASE_URL}/api/document_general/{docg_id}/"
    departments_url = f"{DATABASE_URL}/api/list/departments/"
    document_format_url = f"{DATABASE_URL}/api/list/Document_format/"
    update_url = f"{DATABASE_URL}/api/document_general/{docg_id}/"

    if request.method == 'GET':
        try:
            document = requests.get(document_url).json()
            departments = requests.get(departments_url).json()
            document_format = requests.get(document_format_url).json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            document, departments, document_format = {}, [], []
            
        return render(request, 'documents/update_documentGen.html', {
            'document': document,
            'departments': departments,
            'Document_format': document_format,
            'database_url': DATABASE_URL,  
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
    

    return render(request, "test.html",{
        'database_url': DATABASE_URL,
    })

def form_emp(request):
    return render(request, 'employee/form_emp.html',{
        'database_url': DATABASE_URL,  
    })

def form_post(request):
    return render(request, 'form_post.html',)

def post(request):
    return render(request, 'post.html',)

def testttt(request):
    return render(request, 'testttt.html',)

def view_emp(request):
    return render(request, 'employee/view_emp.html',
                  { 'database_url': DATABASE_URL, })
import requests
import json
import logging
from django.http import JsonResponse
from django.shortcuts import render

logger = logging.getLogger(__name__)

def update_emp(request, emp_id):
    base_url = f"{DATABASE_URL}/api/employee/{emp_id}/"
    departments_url = f"{DATABASE_URL}/api/list/departments/"
    positions_url = f"{DATABASE_URL}/api/positions/"

    if request.method == 'GET':
        data = {
            'employee': {},
            'personal_information': [],
            'education': [],
            'specialized_education': [],
            'political_theory_education': [],
            'foreign_languages': [],
            'work_experiences': [],
            'training_courses': [],
            'awards': [],
            'disciplinary_actions': [],
            'family_members': [],
            'evaluation': {},
        }
        departments = []
        positions = []

        try:
            response = requests.get(base_url)
            response.raise_for_status()
            employee_data = response.json()
            if not employee_data or not isinstance(employee_data, list):
                # logger.error("Invalid employee data format for ID %s", emp_id)
                data['error'] = "Invalid employee data format."
            else:
                employee_data = employee_data[0]  # Assuming data is a list
                # logger.debug("Fetched employee data for ID %s: %s", emp_id, employee_data)

                data['employee'] = employee_data.get('employee', {})
                data['personal_information'] = employee_data.get('personal_information', [])
                data['education'] = employee_data.get('education', [])
                data['specialized_education'] = employee_data.get('specialized_education', [])
                data['political_theory_education'] = employee_data.get('political_theory_education', [])
                data['foreign_languages'] = employee_data.get('foreign_languages', [])
                data['work_experiences'] = employee_data.get('work_experiences', [])
                data['training_courses'] = employee_data.get('training_courses', [])
                data['awards'] = employee_data.get('awards', [])
                data['disciplinary_actions'] = employee_data.get('disciplinary_actions', [])
                data['family_members'] = employee_data.get('family_members', [])
                data['evaluation'] = employee_data.get('evaluation', {})

        except requests.exceptions.RequestException as e:
            # logger.error("Error fetching employee data for ID %s: %s", emp_id, str(e))
            data['error'] = "Failed to fetch employee data."

        try:
            response = requests.get(departments_url)
            response.raise_for_status()
            departments = response.json()
            # logger.debug("Fetched departments: %s", departments)
        except requests.exceptions.RequestException as e:
            # logger.error("Error fetching departments: %s", str(e))
            departments = []
        try:
            response = requests.get(positions_url)
            response.raise_for_status()
            positions = response.json()
            # logger.debug("Fetched positions: %s", positions)
        except requests.exceptions.RequestException as e:
            # logger.error("Error fetching positions: %s", str(e))
            positions = []

        return render(request, 'employee/update_emp.html', {
            **data,
            'positions': positions,
            'departments': departments,
            'database_url': DATABASE_URL,
            'emp_id': emp_id,
        })

    
def homeSalary(request):
    return render(request, "calculate salary/home_salary.html",{
        'database_url': DATABASE_URL,
    })
def baseSalary(request):
    return render(request, "calculate salary/base_salary.html",{
        'database_url': DATABASE_URL,
    }) 
def subsidyPosition(request):
    return render(request, "calculate salary/subsidy_position.html",{
        'database_url': DATABASE_URL,
    })
def workerSubsidy(request):
    return render(request, "calculate salary/worker_subsidy.html",{
        'database_url': DATABASE_URL,
    })
def fuelSubsidy(request):
    return render(request, "calculate salary/fuel_subsidy.html",{
        'database_url': DATABASE_URL,
    })  
def calculateOt(request):    
    return render(request, "calculate salary/calculate_ot.html",{
        'database_url': DATABASE_URL,
    })
def calculateFuel(request):
    return render(request, "calculate salary/calculate_fuel.html",{
        'database_url': DATABASE_URL,
    })
def calculateSalary(request):
    return render(request, "calculate salary/calculate_salary.html",{
        'database_url': DATABASE_URL,
    })
def calculateFood(request):
    return render(request, "calculate salary/calculate_food.html",{
        'database_url': DATABASE_URL,
    })
def reportSupFood(request):
    return render(request, "calculate salary/report_sup_food.html",{
        'database_url': DATABASE_URL,
    })
def reportFuel(request): 
    return render(request, "calculate salary/report_fuel.html",{
        'database_url': DATABASE_URL,
    })
def reportOt(request):
    return render(request, "calculate salary/report_ot.html",{
        'database_url': DATABASE_URL,
    })