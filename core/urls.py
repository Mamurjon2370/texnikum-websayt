from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("biz-haqimizda/", views.about, name="about"),
    path("yonalishlar/", views.programs, name="programs"),
    path("yonalishlar/<slug:slug>/", views.program_detail, name="program_detail"),
    path("qabul/", views.admissions, name="admissions"),
    path("yangiliklar/", views.news_list, name="news_list"),
    path("yangiliklar/<slug:slug>/", views.news_detail, name="news_detail"),
    path("galereya/", views.gallery, name="gallery"),
    path("aloqa/", views.contact, name="contact"),
    path("qidiruv/", views.search, name="search"),
]
