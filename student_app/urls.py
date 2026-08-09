from django.urls import path
from . import views


urlpatterns=[
    path('login/',views.student_login,name='student_login' ),
    path('logout/',views.student_logout,name='student_logout' ),
    path("success/",views.student_success,name="student_success"),
    path('register/', views.register, name='student_register' ),
    path('profile/', views.student_profile, name='student_profile'),
    path("edit-profile/", views.edit_student_profile, name="edit_student_profile"),
    path("resume_analysis/", views.resume_analysis, name="resume_analysis"),
    path("applied-jobs/", views.applied_jobs, name="applied_jobs"),
    path("apply-job/<int:job_id>/", views.apply_job, name="apply_job"),
    path("jobs/", views.student_jobs, name="student_jobs"),
    path("my-applications/",views.my_applications,name="my_applications"),
    
]