from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("analysis/", views.analysis, name="analysis"),
    path("predict/", views.analyze_resume, name="predict"),
    path("team/", views.team, name="team"),
    path("contact/", views.contact, name="contact"),
]
