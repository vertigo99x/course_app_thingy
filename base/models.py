from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


class Courses(models.Model):
    course_code = models.CharField(max_length=255, null=True)
    course_title = models.CharField(max_length=255, null=True)
    course_lecturer = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.course_code}"
    

    

class CourseMaterial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, null=True)
    course_code = models.CharField(max_length=255, null=True)
    file = models.FileField(upload_to='course_materials/', null=True)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.filename} -> {self.created}"
    
    class Meta:
        ordering = ['-created']
        
        
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=255, null=True)
    is_complete = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.task} -> {self.created}"
    
    class Meta:
        ordering = ['-created']
    
class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, null=True)
    course_code = models.CharField(max_length=255, null=True)
    file = models.FileField(upload_to='course_materials/', null=True)
    is_complete = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.filename} -> {self.is_complete} -> {self.created}"
    
    class Meta:
        ordering = ['-created']


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    firstname = models.CharField(max_length=255, null=True, default='')
    lastname = models.CharField(max_length=255, null=True, default='')
    othername = models.CharField(max_length=255, null=True, default='')
    level = models.CharField(max_length=255, null=True, default='')
    dept = models.CharField(max_length=255, null=True, default='')
    email = models.CharField(max_length=255, null=True, default='')
    college = models.CharField(max_length=255, null=True, default='')
    matric_no = models.CharField(max_length=255, null=True, default='')
    
    
    def __str__(self):
        return f"{self.matric_no} -> {self.lastname} {self.firstname}"