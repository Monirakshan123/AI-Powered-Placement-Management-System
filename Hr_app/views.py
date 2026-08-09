from django.shortcuts import render, redirect
from .models import HRProfile,Post_Job
from django.db.models import Avg, Max
from django.utils import timezone
from .models import Notification
from student_app.models import StudentProfile
from django.shortcuts import get_object_or_404
from student_app.models import JobApplication
from .ai_resume import extract_resume_text, calculate_match_score

from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def Hr_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        company_name = request.POST.get("company_name")
        job = request.POST.get("job")
    

        if HRProfile.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already registered. Please use another email."
            )

            return render(
                request,
                "Hr_app/register.html"
            )



        HRProfile.objects.create(
            name=name,
            email=email,
            password=password,
            company_name=company_name,
            job=job
        )


        return redirect("hr_success")


    return render(
        request,
        "Hr_app/register.html"
    )


def hr_success(request):

    return render(
        request,
        "Hr_app/success.html"
    )
def Hr_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")


        hr = HRProfile.objects.filter(
            email=email,
            password=password
        ).first()


        if hr:
            if hr.status!='Approved':
                return render( 
                          request, 
                          'Hr_app/login.html', 
                          {'error': 'Your company is awaiting admin approval.'} 
                          )
            

            else:
                request.session["hr_id"] = hr.id
                return redirect("hr_dashboard")



    return render(
        request,
        "Hr_app/login.html"
    )
    

from student_app.models import JobApplication

def hr_dashboard(request):
    if "hr_id" not in request.session:
        return redirect("Hr_login")

    hr = HRProfile.objects.get(
    id=request.session["hr_id"]
)
    
    applications = JobApplication.objects.filter(
    job__company=hr)

    hr = HRProfile.objects.get(
        id=request.session["hr_id"]
    )

    jobs = Post_Job.objects.filter(
        company=hr
    )

    applications = JobApplication.objects.filter(
        job__company=hr
    )

    total_jobs = jobs.count()

    total_applicants = applications.count()

    shortlisted = applications.filter(
        status="Shortlisted"
    ).count()

    rejected = applications.filter(
        status="Rejected"
    ).count()

    average_score = applications.aggregate(
        Avg("ai_score")
    )["ai_score__avg"]

    highest_score = applications.aggregate(
        Max("ai_score")
    )["ai_score__max"]
    total_applications = applications.count()

    excellent = applications.filter(
    ai_recommendation="Excellent Match"
).count()

    good = applications.filter(
    ai_recommendation="Good Match"
).count()

    average = applications.filter(
    ai_recommendation="Average Match"
).count()

    poor = applications.filter(
    ai_recommendation="Poor Match"
).count()

   
   
    notifications = Notification.objects.filter(is_read=False)[:10]
    context = {
        "hr": hr,
        "total_jobs": total_jobs,
        "total_applicants": total_applicants,
        "total_applications": total_applications,
        "shortlisted": shortlisted,
        "rejected": rejected,
        "average_score": round(average_score or 0),
        "highest_score": highest_score or 0,
        "excellent": excellent,
        "good": good,
        "average": average,
        "poor": poor,
        "notifications": notifications,
}

    return render(
    request,
    "Hr_app/hr_dashboard.html",
    context
)


   
def post_job(request):


    hr = HRProfile.objects.get(
        id=request.session["hr_id"]
    )


    if request.method=="POST":


        Post_Job.objects.create(


            job_title=request.POST.get("job_title"),

            company=hr,

            description=request.POST.get("description"),

            skills=request.POST.get("skills_required"),

            qualification=request.POST.get("qualification"),

            salary=request.POST.get("salary"),

            location=request.POST.get("location"),

            deadline=request.POST.get("deadline")

        )
        Notification.objects.create(
    title="New Job Posted",
    message=f"{job.job_title} has been posted.",
    link="/hr/posted-jobs/"
)


        return redirect("posted_jobs")



    return render(
        request,
        "Hr_app/Post_job.html"
    )
from .models import Post_Job

def posted_jobs(request):

    if "hr_id" not in request.session:
        return redirect("Hr_login")

    hr = HRProfile.objects.get(id=request.session["hr_id"])

    jobs = Post_Job.objects.filter(company=hr).order_by("-posted_at")

    return render(
        request,
        "Hr_app/posted_jobs.html",
        {
            "jobs": jobs
        }
    )
def edit_job(request, id):

    if "hr_id" not in request.session:
        return redirect("Hr_login")

    hr = HRProfile.objects.get(id=request.session["hr_id"])

    job = Post_Job.objects.get(id=id, company=hr)

    if request.method == "POST":

        job.job_title = request.POST.get("job_title")
        job.location = request.POST.get("location")
        job.salary = request.POST.get("salary")
        job.job_type = request.POST.get("job_type")
        job.experience = request.POST.get("experience")
        job.qualification = request.POST.get("qualification")
        job.skills = request.POST.get("skills")
        job.description = request.POST.get("description")
        job.deadline = request.POST.get("deadline")

        job.save()

        return redirect("posted_jobs")

    return render(
        request,
        "Hr_app/edit_job.html",
        {"job": job}
    )
from django.shortcuts import render, redirect, get_object_or_404
from .models import HRProfile, Post_Job

from django.shortcuts import get_object_or_404

def delete_job(request, id):

    if "hr_id" not in request.session:
        return redirect("Hr_login")

    hr = HRProfile.objects.get(id=request.session["hr_id"])

    job = get_object_or_404(
        Post_Job,
        id=id,
        company=hr
    )

    if request.method == "POST":
        job.delete()

    return redirect("posted_jobs")

def Hr_logout(request):

    return redirect(
        'Hr_login'
    )
def hr_profile(request):

    if "hr_id" not in request.session:
        return redirect("Hr_login")

    hr = HRProfile.objects.get(
        id=request.session["hr_id"]
    )

    return render(
        request,
        "Hr_app/hr_profile.html",
        {
            "hr": hr
        }
    )
def edit_hr_profile(request):

    if "hr_id" not in request.session:
        return redirect("Hr_login")

    hr = HRProfile.objects.get(
        id=request.session["hr_id"]
    )

    if request.method == "POST":

        hr.name = request.POST.get("name")

        hr.company_name = request.POST.get("company_name")

        hr.email = request.POST.get("email")

        hr.save()

        return redirect("hr_profile")

    return render(
        request,
        "Hr_app/edit_hr_profile.html",
        {
            "hr": hr
        }
    )
def all_applicants(request):

    if "hr_id" not in request.session:
        return redirect("Hr_login")

    hr = HRProfile.objects.get(
        id=request.session["hr_id"]
    )

    applications = JobApplication.objects.filter(
        job__company=hr
    ).order_by("-ai_score","-applied_at")

    return render(
        request,
        "Hr_app/all_applicants.html",
        {
            "applications": applications
        }
    )
from django.shortcuts import get_object_or_404, render, redirect
from student_app.models import StudentProfile

def student_profile(request, student_id):

    if "hr_id" not in request.session:
        return redirect("Hr_login")

    student = get_object_or_404(StudentProfile, id=student_id)

    return render(
        request,
        "student_app/profile.html",
        {
            "student": student,
            "hr_view": True
        }
    )
def shortlist_applicant(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id
    )

    application.status = "Shortlisted"

    application.save()

    return redirect("all_applicants")
def reject_applicant(request, application_id):

    application = get_object_or_404(
        JobApplication,
        id=application_id
    )

    application.status = "Rejected"

    application.save()

    return redirect("all_applicants")
def ai_match(request, application_id):

    if "hr_id" not in request.session:
        return redirect("Hr_login")

    application = get_object_or_404(
        JobApplication,
        id=application_id
    )

    # Check if resume exists
    if not application.student.resume:

        return render(
            request,
            "Hr_app/ai_result.html",
            {
                "error": "Student has not uploaded a resume."
            }
        )

    # Extract resume text
    resume_text = extract_resume_text(
        application.student.resume.path
    )
    if application.student.skills:
        resume_text += " " + application.student.skills

    # Combine job description and required skills
    job_text = (
        application.job.description + " " +
        application.job.skills
    )

    # Calculate similarity
    # TF-IDF Score
    tfidf_score = calculate_match_score(
    job_text,
    resume_text
)

    resume_lower = resume_text.lower().replace(",", " ")

    job_skills = [
    skill.strip()
    for skill in application.job.skills.split(",")
]

    matching_skills = []
    missing_skills = []

    for skill in job_skills:
        if skill.lower() in resume_lower:
            matching_skills.append(skill)
        else:
           missing_skills.append(skill)

# Skill Match Score
    total_skills = len(job_skills)

    if total_skills > 0:
        skill_score = round(
        (len(matching_skills) / total_skills) * 100
    )
    else:
      skill_score = 0

# Final ATS Score
    score = round(
    (skill_score * 0.8) +
    (tfidf_score * 0.2)
)
    if score >= 80:
        recommendation = "Excellent"

    elif score >= 60:
        recommendation = "Good"

    elif score >= 40:
        recommendation = "Average"

    else:
        recommendation = "Poor"
    application.ai_score = score
    application.ai_recommendation = recommendation
    application.analysis_date = timezone.now()
    application.save()
    
    Notification.objects.create(
    title="AI Screening Completed",
    message=f"AI completed screening for {application.student.name}",
    link=f"/hr/ai_match/{application.id}/"
)

    return render(
        request,
        "Hr_app/ai_result.html",
        {
            "application": application,
            "score": score
        }
    )