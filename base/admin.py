from django.contrib import admin

from .models import Courses, Assignment, CourseMaterial, Task, UserData


model_list = [Courses, Assignment, CourseMaterial, Task, UserData]

for item in model_list:
    admin.site.register(item)