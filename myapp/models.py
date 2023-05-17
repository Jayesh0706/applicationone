from django.db import models

# Create your models here.
class Register(models.Model):
    firstname=models.CharField(max_length=100,default="")
    lastname=models.CharField(max_length=100,default="")
    city=models.CharField(max_length=100,default="")
    mobileno=models.BigIntegerField(default=0)
    emailid=models.EmailField(max_length=100,default="")
    password=models.CharField(max_length=100,default="")
    