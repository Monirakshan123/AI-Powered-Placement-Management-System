
from . import views
from django.contrib import admin 
from django.urls import path, include


urlpatterns =[
    path('register/',views.admin_register,name='admin_register'),
    path('login/',views.admin_login,name='admin_login'),
    path('dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('logout/',views.admin_logout,name="admin_logout"),
    path('students/',views.admin_students,name='admin_students'),
    path('students/delete/<int:id>/',views.delete_student,name='delete_student'),
    path('institutions/',views.admin_institutions,name='admin_institutions'),
    path('institutions/approve/<int:id>/',views.approve_institution,name='approve_institution'),
    path('institutions/reject/<int:id>/',views.reject_institution,name='reject_institution'),
    path('companies/',views.admin_companies,name='admin_companies'),
    path('companies/approve/<int:id>/',views.approve_company,name='approve_company'),
    path('companies/reject/<int:id>/',views.reject_company,name='reject_company'),
    


]