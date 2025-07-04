from django.shortcuts import redirect
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from frontend.views import documentEntry
from frontend import views
from frontend.views import add_documentO

# from frontend.views import form_login
def redirect_to_login(request):
    return redirect('/login/')

urlpatterns = [ 
    path('', redirect_to_login), 
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('index1/', views.index1, name='index1'),

    path('form_emp/', views.form_emp, name='form_emp'),
    path('tables_emp/', views.tables_emp, name='tables_emp'),
    path('update_emp/<int:emp_id>/', views.update_emp, name='update_emp'),
    path('view_emp/', views.view_emp, name='view_emp'),
    path('print_emp/<int:emp_id>/', views.print_emp, name='print_emp'),

    path('login/', views.form_login, name='form_login'),
    path('profile/', views.profile, name='profile'), 
    path('register/',views.register, name='register'),
    
    path('form_post/', views.form_post, name='form_post'),
    path('post', views.post, name='post'),
    path('doc_format/', views.doc_format, name='doc_format'),
    
    path('documentEntry/', documentEntry, name='document_entry'),
    path('department/', views.department, name='department'),
    path('position/', views.position, name='position'),
    path('salary_grade/', views.salary_grade, name='salary_grade'),
    path('documentEntry/', views.documentEntry, name='documentEntry'),
    path('documentOut/', views.documentOut, name='documentOut'),
    path('add_documentE/', views.add_documentE, name='add_documentE'),
    path('add_documentO/', add_documentO, name='add_documentO'),
    path('add_documentG/', views.add_documentG, name='add_documentG'),
    path('documentGen/',views.documentGen, name='documentGen'),
    path('view_post/', views.view_post, name='view_post'),
    path('update_documentGen/<int:docg_id>/', views.update_documentGen, name='update_documentGen'),
    path('test/', views.test_view, name='test'),
    
    path('update_documentO/<int:doc_id>/', views.update_documentO, name='update_documentO'),
    path('update_documentE/<int:doc_id>/', views.update_documentE, name='update_documentE'),
   
    path('homeSalary/', views.homeSalary, name='homeSalary'),
    path('baseSalary/', views.baseSalary, name='baseSalary'),
    path('subsidyPosition/', views.subsidyPosition, name='subsidyPosition'),
    path('workerSubsidy/', views.workerSubsidy, name='workerSubsidy'),
    path('fuelSubsidy/', views.fuelSubsidy, name='fuelSubsidy'),

    path('calculateOt/', views.calculateOt, name='calculcateOt'),
    path('calculateFuel/', views.calculateFuel, name='calculateFuel'),
    path('calculateSalary/', views.calculateSalary, name='calculateSalary'),
    path('calculateFood/', views.calculateFood, name='calculateFood'),
    path('specialAllowances/', views.specialAllowances, name='specialSallowances'),
    path('cal_SpecialAllowces/', views.cal_SpecialAllowces, name='cal_SpecialAllowces'),

    path('reportSalary/', views.reportSalary, name='reportSalary'),
    path('reportSupFood/', views.reportSupFood, name='reportSupFood'),
    path('reportFuel/', views.reportFuel, name='reportFuel'),
    path('reportOt/', views.reportOt, name='reportOt'),
]
