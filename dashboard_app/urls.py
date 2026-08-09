from django.urls import path
from . import views


urlpatterns = [

    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    # urls.py
    path("logout/", views.logout_view, name="logout"),
    path("jobs/", views.student_jobs, name="student_jobs"),
]