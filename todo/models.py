from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name="tasks")
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        order_with_respect_to = "user"
        
