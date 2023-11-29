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
        df = pd.DataFrame(list(patient_count_over_time))
        df['date'] = pd.to_datetime(df['date_joined__date'])

        app = DjangoDash('SimpleExample')
        # Create layout for Dash app
        app.layout = html.Div([
            dcc.Graph(
                id='line-graph',
                figure=px.line(df, x='date', y='patient_count', title='Count over Time')
            )
        ])
        
        # Count of total patients assigned to the doctor
        num_patients = patients_assigned_to_doctor.count()

        return render(request, 'polls/homepage.html', {'patient_count_over_time': patient_count_over_time, 'num_patients': num_patients})
    else:
        return redirect('/')






def patients(request):
    if request.user.user_type == "doctor":
        patients_assigned_to_doctor = CustomUser.objects.filter(assigned_doctor=request.user)

        return render(request, 'polls/patients.html', {'patients': patients_assigned_to_doctor})
    else:
        return redirect('/')
    




    
@login_required(login_url='polls:custom_login')
def games(request):
    # Add any context data or logic needed for the games page
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
