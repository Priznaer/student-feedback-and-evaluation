from django.urls import path
from . import views



urlpatterns = [
    path("", views.login_page, name="login_page"),
    path("home/", views.homepage, name="homepage"),
    path("help/", views.help_page, name="help_page"),
    path("done/", views.done_page, name="done_page"),
    path("create-feedback/", views.create_feedback, name="create_feedback"),
    path("feedback/<uuid:feedback_pk>", views.view_feedback, name="feedback_detail"),
    path("register/", views.register, name="register"),
    path("generate-report/", views.generate_report, name="generate_report"),
    path('get_courses/', views.get_courses, name='get_courses'),
    path('get_lecturers/', views.get_lecturers, name='get_lecturers'),
    path("report/<uuid:report_pk>", views.view_report, name="view_report"),
    path("logout/", views.logout_user, name="logout"),
]