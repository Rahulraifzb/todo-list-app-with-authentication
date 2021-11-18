from django.urls import path 
from .views import *

urlpatterns = [ 
    path("",TaskListView.as_view(),name="tasks"),
    path("register/",RegisterView.as_view(),name="register"),
    path("login/",CustomLoginView.as_view(),name="login"),
]