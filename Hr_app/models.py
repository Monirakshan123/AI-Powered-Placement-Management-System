from django.db import models


class HRProfile(models.Model):

    name = models.CharField(
        max_length=100
    )
    company_name = models.CharField(max_length=150)
    job = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    email = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=100
    )
    status = models.CharField( max_length=20, default='Pending' )




    def __str__(self):
        return self.name

from django.db import models

class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    link = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class Post_Job(models.Model):
    company = models.ForeignKey(HRProfile, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    job_type = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    qualification = models.CharField(max_length=100)
    skills = models.TextField()
    description = models.TextField()
    deadline = models.DateField()
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.job_title