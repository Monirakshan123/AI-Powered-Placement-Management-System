from django.urls import path
from . import views


urlpatterns = [

    path('register/',views.register,name="institution_register" ),
    path("dashboard/",views.institution_dashboard,name="institution_dashboard"),
    path( "login/", views.institution_login, name="institution_login"),
    path("students/",views.institution_students,name="institution_students"),
    path("companies/",views.institution_companies,name="institution_companies"),
    path("jobs/",views.institution_jobs,name="institution_jobs"),
    path("analytics/",views.institution_analytics,name="institution_analytics"),
    path("reports/",views.institution_reports,name="institution_reports"),
    path("profile/",views.institution_profile,name="institution_profile"),
    path("logout/",views.institution_logout,name="institution_logout"),
    path(
    "download/students/",
    views.download_students_report,
    name="download_students_report"
),

path("download/companies/",views.download_companies_report,name="download_companies_report"),
path("download/jobs/", views.download_jobs_report, name="download_jobs_report"),
path("download/applications/",views.download_applications_report,name="download_applications_report"),
path('students/',views.institution_students,name='institution_students'),
path('students/approve/<int:id>/',views.approve_student,name='approve_student'),
path('students/reject/<int:id>/',views.reject_student,name='reject_student'),

]