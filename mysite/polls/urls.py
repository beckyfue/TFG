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

]
