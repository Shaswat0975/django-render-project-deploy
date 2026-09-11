from django.db import models

# Create your models here.

class Student(models.Model):
    name=models.CharField(max_length=30,null=True)
    email=models.CharField(max_length=30,null=True)
    username=models.CharField(max_length=30,unique=True,null=True)
    password=models.CharField(max_length=30,null=True)
    college=models.CharField(max_length=90,null=True)
    city=models.CharField(max_length=30,null=True)
    jdate=models.CharField(max_length=30,null=True)
    total_fee=models.CharField(max_length=30,null=True)
    paid_fee=models.CharField(max_length=30,null=True)
    left_fee=models.CharField(max_length=30,null=True)
    phone=models.CharField(max_length=30,null=True)
    technology=models.CharField(max_length=30,null=True)
    image=models.FileField(max_length=30,null=True)

class Feedback(models.Model):
    name=models.CharField(max_length=30,null=True)
    email=models.CharField(max_length=30,null=True)
    feedback=models.TextField(max_length=100,null=True)