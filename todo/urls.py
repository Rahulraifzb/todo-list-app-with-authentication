from django.urls import path 
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",CustomLoginView.as_view(),name="login"), 
    path("logout/",LogoutView.as_view(next_page='login'),name="logout"),

    path("",TaskListView.as_view(),name="task-list"),
    path("create/",TaskCreateView.as_view(),name="task-create"),
    path("<str:pk>/",TaskDetailView.as_view(),name="task-detail"),
    path("<str:pk>/update/",TaskUpdateView.as_view(),name="task-update"),
    path("<str:pk>/delete/",TaskDeleteView.as_view(),name="task-delete"),
]