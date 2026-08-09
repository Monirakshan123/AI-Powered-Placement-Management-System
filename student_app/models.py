from django.db import models
from Hr_app.models import Post_Job
from django.contrib.auth.models import User

class StudentProfile(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=100)

    college = models.CharField(max_length=150, blank=True)

    department = models.CharField(max_length=100, blank=True)
    
    status = models.CharField( max_length=20, default='Pending' )
    
    registerno = models.CharField(max_length=30,unique=True,null=True,blank=True) 
       
    year = models.CharField(max_length=20, blank=True)

    cgpa = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )

    skills = models.TextField(blank=True)

    resume = models.FileField(
        upload_to="resumes/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
class Job(models.Model):
    title = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class StudentResume(models.Model):
    user = models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    resume = models.FileField(upload_to="resumes/")


class Application(models.Model):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Selected", "Selected"),
        ("Rejected", "Rejected"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
from Hr_app.models import Post_Job

class JobApplication(models.Model):

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    job = models.ForeignKey(
        Post_Job,
        on_delete=models.CASCADE
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        default="Applied"
    )
    ai_score = models.IntegerField(
    null=True,
    blank=True
)

    ai_recommendation = models.CharField(
    max_length=50,
    blank=True
)

    analysis_date = models.DateTimeField(
    null=True,
    blank=True
)

    class Meta:
        unique_together = ("student", "job")

    def __str__(self):
        return f"{self.student.name} - {self.job.job_title}"

def student_jobs(request):

    if "student_id" not in request.session:
        return redirect("Student_login")

    jobs = Post_Job.objects.all().order_by("-posted_at")

    return render(
        request,
        "student_app/student_jobs.html",
        {
            "jobs": jobs
        }
    )