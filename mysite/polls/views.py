from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomRegistrationForm
from django.contrib import messages



def index(request):
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


def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data['user_type']
            login(request, user)
            if user_type == 'patient':
                return render(request, 'polls/patientdash.html')
            elif user_type == 'doctor':
                return render(request, 'polls/doctordash.html')
            if user_type == 'admin':
                return render(request, 'polls/admindash.html')
        
    else:
        form = CustomRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



   