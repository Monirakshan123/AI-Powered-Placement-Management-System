from django.urls import path
from . import views


urlpatterns = [

    path('register/',views.Hr_register,name="Hr_register" ),
    path("success/",views.hr_success,name="hr_success"),
    path("login/",views.Hr_login,name="Hr_login"),
    path("dashboard/",views.hr_dashboard,name="hr_dashboard"),
    path("Post_Job/",views.post_job,name="Post_Job"),
    path("posted-jobs/", views.posted_jobs, name="posted_jobs"),
    path("edit_job/<int:id>/", views.edit_job, name="edit_job"),
    path("delete_job/<int:id>/", views.delete_job, name="delete_job"),
    path("logout/",views.Hr_logout,name="Hr_logout"),
    path("profile/",views.hr_profile,name="hr_profile"),
    path("edit-profile/",views.edit_hr_profile,name="edit_hr_profile"),
    path("applicants/",views.all_applicants,name="all_applicants"),
    path("student/<int:student_id>/",views.student_profile,name="student_profile"),
    path("shortlist/<int:application_id>/",views.shortlist_applicant,name="shortlist_applicant"),
    path("reject/<int:application_id>/",views.reject_applicant,name="reject_applicant"),
    path("ai_match/<int:application_id>/",views.ai_match,name="ai_match"),
]