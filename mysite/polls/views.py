from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, CustomUser
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PatientCreationForm
import json


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
    return render(request, 'registration/register2.html', {'form': form, "form_errors": json.loads(form.errors.as_json())})


def custom_login(request):
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
        return render(request, 'polls/login.html')

 

@login_required
def main(request):
    return render(request, 'polls/doctordash.html')


@login_required
def create_patient(request):
    if request.user.user_type == "doctor":
        if request.method == 'POST':
            form = PatientCreationForm(request.POST)
            #Check that the form that has been filled out is valid
            if form.is_valid():
                #If form is valid, we create a patient object without saving it in the database
                patient = form.save(commit=False)
                patient.user_type = 'patient'
                #Set the assigned doctor as the one that is currently signed in
                doctor_user = CustomUser.objects.get(id=request.user.id)
                patient.assigned_doctor = doctor_user
                #Now we can save the patient to the database
                patient.save()
                return redirect('polls:main')  
        else: #Then ir would be a GET
            form = PatientCreationForm()

        return render(request, 'polls/create_patient.html', {'form': form})
    else:
        return redirect('/')

