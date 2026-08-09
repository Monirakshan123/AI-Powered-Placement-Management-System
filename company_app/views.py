from django.shortcuts import render,redirect
from .models import AdminProfile 
from student_app.models import StudentProfile 
from Hr_app.models import HRProfile, Post_Job 
from student_app.models import JobApplication
from Institution_app.models import InstitutionProfile # Admin Register 
def admin_register(request): 
    if request.method == 'POST': 
        name = request.POST.get('name') 
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        confirm_password = request.POST.get('confirm_password') 
        if password != confirm_password: 
            return render( request, 'company_app/register.html', {'error': 'Passwords do not match'} ) 
        if AdminProfile.objects.filter(email=email).exists(): 
            return render( request, 'company_app/register.html', {'error': 'Email already exists'} ) 
        AdminProfile.objects.create( name=name, email=email, password=password ) 
        return redirect('admin_login') 
    return render(request, 'company_app/register.html') # Admin Login 

def admin_login(request): 
    if request.method == 'POST': 
        email = request.POST.get('email') 
        password = request.POST.get('password') 
        admin = AdminProfile.objects.filter( email=email, password=password ).first() 
        if admin: 
            request.session['admin_id'] = admin.id 
            return redirect('admin_dashboard') 
        return render( request, 'company_app/login.html', {'error': 'Invalid email or password'} ) 
    return render(request, 'company_app/login.html') # Admin Dashboard
 
def admin_dashboard(request): 
    if 'admin_id' not in request.session: 
        return redirect('admin_login') 
    admin = AdminProfile.objects.get( id=request.session['admin_id'] ) 
    context = { 'admin': admin, 'total_students': StudentProfile.objects.count(), 'total_companies': HRProfile.objects.count(), 'total_institutions': InstitutionProfile.objects.count(), 'total_jobs': Post_Job.objects.count(), 'total_applications': JobApplication.objects.count(), } 
    return render( request, 'company_app/dashboard.html', context ) # Admin Logout 

def admin_logout(request): 
    request.session.flush() 
    return redirect('admin_login')

def admin_students(request): 
    if 'admin_id' not in request.session: 
        return redirect('admin_login') 
    students = StudentProfile.objects.all().order_by('-id') 
    return render( request, 'company_app/students.html', { 'students': students } )

def delete_student(request, id): 
    if 'admin_id' not in request.session: 
        return redirect('admin_login') 
    student = StudentProfile.objects.get(id=id) 
    student.delete() 
    return redirect('admin_students')

def admin_institutions(request): 
    if 'admin_id' not in request.session: 
        return redirect('admin_login') 
    institutions = InstitutionProfile.objects.all().order_by('-id') 
    return render( request, 'company_app/institutions.html', { 'institutions': institutions } )

def approve_institution(request, id):
    if 'admin_id' not in request.session: 
        return redirect('admin_login') 
    institution = InstitutionProfile.objects.get(id=id) 
    institution.status = 'Approved' 
    institution.save() 
    return redirect('admin_institutions')

def reject_institution(request, id): 
    if 'admin_id' not in request.session: 
        return redirect('admin_login') 
    institution = InstitutionProfile.objects.get(id=id) 
    institution.status = 'Rejected' 
    institution.save() 
    return redirect('admin_institutions')

def admin_companies(request): 
    if 'admin_id' not in request.session: 
        return redirect('admin_login') 
    companies = HRProfile.objects.all().order_by('-id') 
    return render( request, 'company_app/companies.html', { 'companies': companies } )

def approve_company(request, id): 
    if 'admin_id' not in request.session: 
        return redirect('admin_login') 
    company = HRProfile.objects.get(id=id) 
    company.status = 'Approved' 
    company.save() 
    return redirect('admin_companies')

def reject_company(request, id): 
    if 'admin_id' not in request.session: 
        return redirect('admin_login') 
    company = HRProfile.objects.get(id=id) 
    company.status = 'Rejected' 
    company.save() 
    return redirect('admin_companies')