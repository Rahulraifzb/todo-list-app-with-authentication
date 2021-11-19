from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.views.generic.edit import BaseUpdateView

from todo.models import Task

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].widget.attrs.update({"placeholder":"John Deo","class":"form-control"})
        self.fields["email"].widget.attrs.update({"placeholder":"john@gmail.com","class":"form-control","required":True})
        self.fields["password1"].widget.attrs.update({"placeholder":"********","class":"form-control"})
        self.fields["password2"].widget.attrs.update({"placeholder":"********","class":"form-control"})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder":"John Deo","class":"form-control"})
        self.fields["password"].widget.attrs.update({"placeholder":"********","class":"form-control"})

    def clean_username(self,*args,**kwargs):
        username = self.cleaned_data.get("username")
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'username does not exists')
        return username

    def clean_password(self,*args,**kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if user := User.objects.filter(username=username).first():
            if not user.check_password(password):
                raise forms.ValidationError('password is incorrect')
            return password

class CustomUpdateFormView(BaseUpdateView):
    class Meta:
        model = Task
        fields = ["title","description","complete"]
    