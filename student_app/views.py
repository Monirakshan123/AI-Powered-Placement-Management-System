from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect,get_object_or_404
from .models import StudentResume
from Hr_app.models import Notification
from Hr_app.models import Post_Job
from Hr_app.ai_resume import extract_resume_text, calculate_match_score
from .models import Post_Job
from .models import JobApplication
from django.contrib.auth.models import User
from .models import StudentProfile
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from Institution_app.models import InstitutionProfile
from django.contrib.auth.decorators import login_required

from django.contrib import messages

def register(request):
    institutions = InstitutionProfile.objects.filter(status='Approved')

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        college = request.POST.get("college")
        department = request.POST.get("department")
        year = request.POST.get("year")
        cgpa = request.POST.get("cgpa")
        skills = request.POST.get("skills")

        if StudentProfile.objects.filter(email=email).exists():
            print("EMail already exists")
            messages.warning(
                request,
                "This email is already registered. Please use another email or login."
            )
            return redirect("student_register")

        try:
            StudentProfile.objects.create(
                name=name,
                email=email,
                password=password,
                college=college,
                department=department,
                year=year,
                cgpa=cgpa if cgpa else None,
                skills=skills if skills else "",
                status="Pending",
            )

            send_mail(
                subject="RecruitIQ Registration Successful",
                message=f"""
Hello {name},

Your account has been registered successfully on RecruitIQ.

Your account is currently under verification by your institution.

You will receive another email once your account is approved.

Thank you,
RecruitIQ Team
""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            messages.success(
                request,
                "Registration successful! Please check your email for login information and further instructions."
            )

            return redirect("student_login")

        except Exception as e:
            print("error:",e)
            messages.error(request, str(e))
            return redirect("student_register")

    return render(request, "student_app/register.html", {
        "institutions": institutions,
    })

def student_profile(request):

    student_id = request.session.get("student_id")

    if not student_id:
        return redirect("student_login")

    student = StudentProfile.objects.get(id=student_id)

    return render(
        request,
        "Student_app/profile.html",
        {
            "student": student
        }
    )
from django.contrib.auth import authenticate, login

def student_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        student = StudentProfile.objects.filter(
            email=email,
            password=password
        ).first()

        if student:
            if student.status != 'Approved': 
                return render( request, 'student_app/login.html', {'error': 'Your account is awaiting institution approval.'} )
            
            request.session["student_id"] = student.id
            return redirect("student_dashboard")

        return render(request, "student_app/login.html", {
            "error": "Invalid email or password"
        })

    return render(request, "student_app/login.html")
def student_logout(request):

    logout(request)

    return redirect(
        'student_login'
    )
def student_success(request):

    return render(
        request,
        "student_app/success.html"
    )
def edit_student_profile(request):

    student = StudentProfile.objects.get(id=request.session["student_id"])

    if request.method == "POST":

        student.name = request.POST.get("name")
        student.email = request.POST.get("email")
        student.phone = request.POST.get("phone")
        student.gender = request.POST.get("gender")

        student.college = request.POST.get("college")
        student.department = request.POST.get("department")
        student.year = request.POST.get("year")
        student.cgpa = request.POST.get("cgpa")
        student.skills = request.POST.get("skills")

        if request.FILES.get("profile_photo"):
            student.profile_photo = request.FILES["profile_photo"]

        if request.FILES.get("resume"):
            student.resume = request.FILES["resume"]
            print(request.FILES)

        student.save()

        return redirect("student_profile")

    return render(
        request,
        "student_app/edit_profile.html",
        {"student": student}
    )
def student_dashboard(request):

    if "student_id" not in request.session:
        return redirect("student_login")

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
from django.shortcuts import render, redirect
from student_app.models import StudentProfile
from Hr_app.models import Post_Job
from Hr_app.ai_resume import extract_resume_text, calculate_match_score
def resume_analysis(request):

    if "student_id" not in request.session:
        return redirect("Student_login")

    student = StudentProfile.objects.get(
        id=request.session["student_id"]
    )

    if not student.resume:
        return render(
            request,
            "student_app/resume_analysis.html",
            {
                "student": student,
                "error": "Please upload your resume first."
            }
        )

    # Read Resume
    resume_text = extract_resume_text(
        student.resume.path
    )

    # Include profile skills
    if student.skills:
        resume_text += " " + student.skills

    # Get all jobs
    jobs = Post_Job.objects.all()

    if not jobs.exists():
        return render(
            request,
            "student_app/resume_analysis.html",
            {
                "student": student,
                "error": "No jobs available."
            }
        )

    # -----------------------------
    # Find Best Matching Job
    # -----------------------------

    best_job = None
    highest_tfidf = 0

    for job in jobs:

        job_text = (
            job.description +
            " " +
            job.skills
        )

        tfidf = calculate_match_score(
            job_text,
            resume_text
        )

        if tfidf > highest_tfidf:
            highest_tfidf = tfidf
            best_job = job

    # -----------------------------
    # Skill Matching
    # -----------------------------

    matching_skills = []
    missing_skills = []

    skill_score = 0

    if best_job:

        resume_lower = resume_text.lower().replace(",", " ")

        job_skills = [
            skill.strip()
            for skill in best_job.skills.split(",")
        ]

        for skill in job_skills:

            if skill.lower() in resume_lower:
                matching_skills.append(skill)
            else:
                missing_skills.append(skill)

        total_skills = len(job_skills)

        if total_skills > 0:

            skill_score = round(
                (len(matching_skills) / total_skills) * 100
            )

    # -----------------------------
    # Final ATS Score
    # -----------------------------

    ats_score = round(
        (skill_score * 0.8) +
        (highest_tfidf * 0.2)
    )

    # -----------------------------
    # Suggestions
    # -----------------------------

    suggestions = []

    for skill in missing_skills:
        suggestions.append(f"Learn {skill}")

    suggestions.append("Add more real-world projects.")
    suggestions.append("Include certifications.")
    suggestions.append("Keep your resume to 1-2 pages.")
    suggestions.append("Use strong action verbs.")
    suggestions.append("Tailor your resume for each job application.")

    # -----------------------------
    # Debug
    # -----------------------------

    #print("Resume Text:", resume_text)
    #print("Best Job:", best_job.job_title if best_job else "None")
    #print("TF-IDF:", highest_tfidf)
    #print("Skill Score:", skill_score)
    #print("ATS Score:", ats_score)
    #print("Matching:", matching_skills)
    #print("Missing:", missing_skills)

    # -----------------------------
    # Context
    # -----------------------------

    context = {

        "student": student,

        "ats_score": ats_score,

        "tfidf_score": highest_tfidf,

        "skill_score": skill_score,

        "best_job": best_job,

        "skills": matching_skills,

        "missing_skills": missing_skills,

        "suggestions": suggestions

    }

    return render(
        request,
        "student_app/resume_analysis.html",
        context
    )


def placements(request):
    jobs = Job.objects.all()
    return render(request, "student/placements.html", {"jobs": jobs})


def applied_jobs(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, "student/applied_jobs.html", {"applications": applications})


from .models import StudentProfile, JobApplication
from Hr_app.models import Post_Job
from django.shortcuts import redirect, get_object_or_404

def apply_job(request, job_id):

    if "student_id" not in request.session:
        return redirect("Student_login")

    student = StudentProfile.objects.get(
        id=request.session["student_id"]
    )

    job = get_object_or_404(
        Post_Job,
        id=job_id
    )

    JobApplication.objects.get_or_create(
        student=student,
        job=job
    )
    Notification.objects.create(
    title="New Job Application",
    message=f"{student.name} applied for {job.job_title}",
    link="/hr/applicants/"
)

    return redirect("student_jobs")
def student_jobs(request):

    if "student_id" not in request.session:
        return redirect("Student_login")

    student = StudentProfile.objects.get(
        id=request.session["student_id"]
    )

    jobs = Post_Job.objects.all().order_by("-posted_at")

    applied_jobs = JobApplication.objects.filter(
        student=student
    ).values_list("job_id", flat=True)

    return render(
        request,
        "student_app/student_jobs.html",
        {
            "jobs": jobs,
            "applied_jobs": applied_jobs
        }
    )
from .models import JobApplication

def my_applications(request):

    if "student_id" not in request.session:
        return redirect("Student_login")

    student = StudentProfile.objects.get(
        id=request.session["student_id"]
    )

    applications = JobApplication.objects.filter(
        student=student
    ).order_by("-applied_at")

    return render(
        request,
        "student_app/my_applications.html",
        {
            "applications": applications
        }
    )