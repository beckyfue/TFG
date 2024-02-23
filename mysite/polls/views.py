from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, CustomUser
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import CustomRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PatientCreationForm
import json
from django.contrib.auth import logout as auth_logout
from django.utils import timezone
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from datetime import datetime
from datetime import timedelta
import random
from django_plotly_dash import DjangoDash




def index(request):
    print(request.user.user_type)
    latest_question_list = Question.objects.order_by("-pub_date")[:5]

    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# views.py
from django.contrib.auth import login

def register(request):
    if request.user.is_authenticated:
        return redirect('polls:main')
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:main') 
    else:
        form = CustomRegistrationForm()
    print(form.errors)
    return render(request, 'registration/register.html', {'form': form, "form_errors": json.loads(form.errors.as_json())})



def custom_login(request):
    if request.user.is_authenticated:
        return redirect('polls:main')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:main')  # Redirect to the main dashboard 
        else:
            messages.error(request, 'Invalid username or password', extra_tags='alert alert-danger text-center')
            return render(request, 'polls/login.html')
    else:
        if len(request.META["QUERY_STRING"]) > 0:
            messages.error(request, 'You need to log in first', extra_tags='alert alert-danger text-center')
        
        return render(request, 'polls/login.html')
    


@login_required(login_url='polls:custom_login')
def main(request):
    if request.user.user_type == "doctor":
        patients_assigned_to_doctor = CustomUser.objects.filter(assigned_doctor=request.user)
        for p in patients_assigned_to_doctor:
            print(p.date_joined, type(p.date_joined))
        return redirect('polls:homepage')
    else:
        return redirect('polls:patient_homepage')




@login_required(login_url='polls:custom_login')
def create_patient(request):
    if request.user.user_type == "doctor":
        if request.method == 'POST':
            form = PatientCreationForm(request.POST)
            if form.is_valid():
                patient = form.save(commit=False)
                patient.user_type = 'patient'
                patient.assigned_doctor = request.user
                patient.save()
                messages.success(request, 'Patient successfully created', extra_tags='alert alert-success text-center')
                return redirect('polls:create_patient')  
        else:
            form = PatientCreationForm()

        return render(request, 'polls/create_patient.html', {'form': form})
    else:
        return redirect('/')





@login_required(login_url='polls:custom_login')
def user_logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        messages.success(request, 'Correct Logout', extra_tags='alert alert-info text-center')
    return redirect('polls:custom_login')

from django.db.models import Count

def homepage(request):
    if request.user.user_type == "doctor":
        patients_assigned_to_doctor = CustomUser.objects.filter(assigned_doctor=request.user)
        patient_count_over_time = patients_assigned_to_doctor.values('date_joined__date').annotate(patient_count=Count('id')).order_by('date_joined__date')
        
        # Count of total patients assigned to the doctor
        num_patients = patients_assigned_to_doctor.count()

        has_patients = True
        if num_patients > 0:
            df = pd.DataFrame(list(patient_count_over_time))
        else:
            df = pd.DataFrame([
                {"date_joined__date": datetime.today().strftime('%Y-%m-%d').split(" ")[0], "patient_count": 0},
                {"date_joined__date": (datetime.today() - timedelta(days = 1)).strftime('%Y-%m-%d').split(" ")[0], "patient_count": 0}
                ])
       
        df['date'] = pd.to_datetime(df['date_joined__date'])
        print(df.head())
        app = DjangoDash('SimpleExample')
        # Create layout for Dash app
        app.layout = html.Div([
            dcc.Graph(
                id='line-graph',
                figure=px.line(df, x='date', y='patient_count', title='Count over Time')
            )
        ])

        return render(request, 'polls/homepage.html', {'has_patients': has_patients, 'num_patients': num_patients})
    else:
        return redirect('/')
    
   

def patients(request):
    if request.user.user_type == "doctor":
        patients_assigned_to_doctor = CustomUser.objects.filter(assigned_doctor=request.user)

        # Count of total patients assigned to the doctor
        num_patients = patients_assigned_to_doctor.count()

        return render(request,'polls/patients.html',{'patients': patients_assigned_to_doctor, 'num_patients': num_patients})
    else:
        return redirect('/')














    
@login_required(login_url='polls:custom_login')
def games(request):
    return render(request, 'polls/games.html')



@login_required(login_url='polls:custom_login')
def patient_homepage(request):
    return render(request, 'polls/patient_homepage.html')



from django.shortcuts import render, get_object_or_404
from .forms import PatientEditForm


def patient_detail(request, patient_id):
    patient = get_object_or_404(CustomUser, id=patient_id)

    if request.method == 'POST':
        form = PatientEditForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, 'Changes saved successfully.')
    else:
        form = PatientEditForm(instance=patient)

    return render(request, 'polls/patient_detail.html', {'patient': patient, 'form': form})


def delete_patient(request, patient_id):
    patient = get_object_or_404(CustomUser, id=patient_id)

    if request.method == 'POST':
        # Confirm deletion
        patient.delete()
        messages.success(request, 'Patient deleted successfully.')
        return redirect('polls:patients')  # Redirect to the list of patients

    return render(request, 'polls/delete_patient.html', {'patient': patient})


@login_required(login_url='polls:custom_login')
def vrgame(request):




    precolored_objects = {
        "id_green_pillow_1": "green",
        "id_green_pillow_2": "green",
        "id_green_pillow_3": "green",
        "id_bathtub": "blue",
        "id_dustbin": "blue",
        "id_ottoman": "yellow",
        "id_shoes": "yellow",
        "id_rocket": "red",
        "id_toy_car": "red", 
        "id_truck": "red"
    }



    object_ids = ["id_green_pillow_1", "id_green_pillow_2", "id_green_pillow_3", "id_tissues", 
                    "id_lounge_chair_1", "id_lounge_chair_2", "id_lounge_chair_3", "id_lounge_chair_4","id_lounge_drawers",
                    "id_fridge", "id_kitchen_cupboard", "id_sauce_pan", "id_coffee_machine", "id_kettle", "id_toaster",
                  "id_toy_car", "id_rocket",  "id_football", "id_bedside_table_1","id_wardrobe_1", "id_bed_1",  "id_stool_2", "id_truck", 
                   "id_stool_1", "id_bed_2", "id_lights", "id_mouse" ,"id_guitar", "id_bottle_water","id_shoes", 
                   "id_ottoman","id_hat","id_headphones",   "id_toilet_1", "id_soap", 
                  "id_dustbin", "id_vanity","id_bed_3", "id_main_wardrobe", 
                  "id_main_lamp_2", "id_main_lamp_3", "id_toilet_2", "id_bathtub"] 
    
    selected_object_ids = random.sample(object_ids, 1)
    available_colors = ["blue", "red", "green", "yellow"]
    random_colors = random.sample(available_colors, 1)
    print("slected objects", selected_object_ids)
    print("selected colour", random_colors)

    change_objects = []
    new_color = None


    # Change colour of objets that are colour of random colour chosen but are not in list of selected objects
    for obj_id, obj_color in precolored_objects.items():
        if obj_id not in selected_object_ids and obj_color == random_colors[0]:
            change_objects.append(obj_id)
            if obj_color in available_colors:
                available_colors.remove(obj_color)
                new_color = random.choice(available_colors)

    
    context = {
        'selected_object_ids': json.dumps(selected_object_ids),
        'random_colors': random_colors[0],
        'new_color': new_color,
        'change_objects': json.dumps(change_objects),
    }
    print("VR GAME URL")
    return render(request, 'polls/vrgame.html')
    
