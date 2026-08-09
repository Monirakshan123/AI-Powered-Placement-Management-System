from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .ai_logic import calculate_match_score
from student_app.models import StudentProfile

def admin_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']


        user = authenticate(
            username=username,
            password=password
        )


        if user:

            login(request,user)
            return redirect('dashboard_app/student_dashboard.html')


    return render(
        request,
        'dashboard_app/login.html'
    )
# views.py
def logout_view(request):
    logout(request)
    return redirect("login")




def student_dashboard(request):

    student = StudentProfile.objects.get(
        id=request.session["student_id"]
    )

    return render(
        request,
        "dashboard_app/student_dashboard.html",
        {
            "student": student
        }
    )
def student_jobs(request):
    return redirect("student_app/applied_jobs.html")