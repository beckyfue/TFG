from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:question_id>/", views.detail, name="detail"),
    path("<int:question_id>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('login/', views.custom_login, name='custom_login'), 
    path('register/', views.register, name='register'),
    path('main/', views.main, name='main'), 
    path('create_patient/', views.create_patient, name='create_patient'),
    path('logout/', views.user_logout, name='user_logout'),
    path('homepage/', views.homepage, name='homepage'),
    path('patients/', views.patients, name='patients'),
    path('games/', views.games, name='games'),
    path('patient_homepage/', views.patient_homepage, name='patient_homepage'),



]
