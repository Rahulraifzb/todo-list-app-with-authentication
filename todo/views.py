from django.db.models import fields
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView, FormView,UpdateView
from django.contrib.auth.views import LoginView
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q 

# Create your views here.

class RegisterView(FormView):
    redirect_authenticated_user = True
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("task-list")
    template_name="register.html"

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super().form_valid(form)

    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect("task-list")
        return super().get(*args,**kwargs)

class CustomLoginView(LoginView):
    template_name="login.html"
    form_class = CustomAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task-list')

class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "task-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search = self.request.GET.get("search",None)

        if search:
            context["tasks"] = context["tasks"].filter(Q(title__icontains = search) | Q(description__icontains=search))
            

        return context

class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = "task"
    template_name = "task-detail.html"

class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    fields = ["title","description","complete"]
    template_name = "task-update.html"
    success_url = reverse_lazy('task-list')

    def get_form(self,*args,**kwargs):
        form = super().get_form()
        form.fields["title"].widget.attrs.update({"class":"form-control"})
        form.fields["description"].widget.attrs.update({"class":"form-control","rows":5})
        form.fields["complete"].widget.attrs.update({"class":"form-check-input"})
        return form

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ["title","description","complete"]
    template_name = "task-create.html"
    success_url = reverse_lazy("task-list")

    def get_form(self,*args,**kwargs):
        form = super().get_form(*args,**kwargs)
        form.fields["title"].widget.attrs.update({"class":"form-control"})
        form.fields["description"].widget.attrs.update({"class":"form-control","rows":5})
        form.fields["complete"].widget.attrs.update({"class":"form-check-input"})
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("task-list")
    template_name = "task-delete.html"

    def get_queryset(self,*args,**kwargs):
        owner = self.request.user
        return self.model.objects.filter(user=owner)
