from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import login

# Create your views here.

class RegisterView(FormView):
    redirect_authenticated_user = True
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("tasks")
    template_name="register.html"

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super().form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super().get(*args,**kwargs)

class CustomLoginView(LoginView):
    template_name="login.html"
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "task-list.html"

def mylogin(request):
    return render(request,"login.html")

def home(request):
    return HttpResponse("hello world")
