from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta

from .models import Courses, Assignment, CourseMaterial, Task, UserData
from django.utils import timezone

from django.contrib.auth.hashers import check_password


@login_required
def dashboard(request):
    context = {}
    
    courses = Courses.objects.all().count()
    assignments = Assignment.objects.filter(user=request.user).count()
    tasks = Task.objects.filter(user=request.user, is_complete=False).count()
    courseMaterials = CourseMaterial.objects.filter(user=request.user).count()
    userdata = UserData.objects.filter(user = request.user)[0]
    
    context['courses_no'] = courses
    context['assignments_no'] = assignments
    context['tasks_no'] = tasks
    context['courseMaterials_no'] = courseMaterials
    context['userdata'] = userdata
    
    return render(request, "dashboard.html", context)



@login_required
def tasks(request):
    context = {}
    if request.method == "POST":
        title = request.POST['title']
        
        task = Task.objects.create(
            user=request.user,
            task=title,
        )
        task.save();
        messages.success(request, 'Task Added Successfully')
        return redirect('tasks')
    
    
    userdata = UserData.objects.filter(user = request.user)[0]
    context['userdata'] = userdata
    tasks = Task.objects.filter(user=request.user)
    context['tasks'] = tasks
    context['tasks_no'] = tasks.filter(is_complete = False).count()
    
    return render(request, "tasks.html", context)
        

@login_required
def tasksUpdate(request, pk):
    Task.objects.filter(id=pk).update(is_complete = True)
    messages.info(request, 'Task Completed')
    return redirect('tasks')


@login_required
def tasksDelete(request, pk):
    Task.objects.filter(id=pk).delete()
    messages.success(request, 'Task Deleted Successfully')
    return redirect('tasks')



@login_required
def courseMat(request):
    context = {}
    if request.method == "POST":
        filename = request.POST['filename']
        file = request.FILES['file']
        course_code = request.POST['course']
        
        mat = CourseMaterial.objects.create(
            user=request.user,
            file=file,
            filename=filename,
            course_code = course_code
        )
        mat.save();
        messages.success(request, 'File Added Successfully')
        return redirect('course-mat')
    
    
    userdata = UserData.objects.filter(user = request.user)[0]
    context['userdata'] = userdata
    mat = CourseMaterial.objects.filter(user=request.user)
    context['materials'] = mat
    context['material_no'] = mat.count()
    
    course_codes = Courses.objects.all()
    context['courses'] = course_codes
    
    return render(request, "course_mat.html", context)



@login_required
def courseMatDelete(request, pk):
    CourseMaterial.objects.filter(id=pk).delete()
    messages.success(request, 'Deleted Successfully')
    return redirect('course-mat')


@login_required
def assignment(request):
    context = {}
    if request.method == "POST":
        filename = request.POST['filename']
        file = request.FILES['file']
        course_code = request.POST['course']
        
        assignment = Assignment.objects.create(
            user=request.user,
            file=file,
            filename=filename,
            course_code = course_code
        )
        
        assignment.save();
        messages.success(request, 'Assignment File Added Successfully')
        return redirect('assignments')
    
    
    userdata = UserData.objects.filter(user = request.user)[0]
    context['userdata'] = userdata
    assignment = Assignment.objects.filter(user=request.user)
    context['assignments'] = assignment
    
    context['assignment_no_completed'] = assignment.filter(is_complete=True).count()
    context['assignment_no_pending'] = assignment.filter(is_complete=False).count()
    
    course_codes = Courses.objects.all()
    context['courses'] = course_codes
    
    return render(request, "assignment.html", context)


@login_required
def profile(request):
    context = {}
    
    userdata = UserData.objects.filter(user = request.user)[0]
    context['userdata'] = userdata
    
    return render(request, "profile.html", context)


@login_required
def changePassword(request):
    if request.method == "POST":
        old_password = request.POST['old']
        new_password = request.POST['new1']

        user = User.objects.filter(id=request.user.id)
        userPassword = user.values()[0]['password']
        matchcheck = check_password(old_password, userPassword)
        u = user[0]
        if matchcheck:
            u.set_password(new_password)
            u.save();
            
            messages.info(request, 'Password Changed Completely')
            return redirect('profile')
        
        messages.info(request, 'Incorrect Old Password')
        return redirect('profile')
    return redirect('profile')
        

@login_required
def assignmentUpdate(request, pk):
    Assignment.objects.filter(id=pk).update(is_complete = True)
    messages.info(request, 'Assignment Completed')
    return redirect('assignments')



@login_required
def assignmentDelete(request, pk):
    Assignment.objects.filter(id=pk).delete()
    messages.success(request, 'Deleted Successfully')
    return redirect('assignments')




def login(request):
    if request.method == 'POST':
        username, password = request.POST['username'].strip().replace('/','-'), request.POST['password']
        user = auth.authenticate(username = username, password = password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        
        messages.error(request, 'User Does Not Exist!!')
        return redirect('login')
    
    return render(request, 'login.html')



def registerUser(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        othername = request.POST['othername']
        level = request.POST['level']
        dept = request.POST['dept']
        email = request.POST['email']
        college = request.POST['college']
        password = request.POST['password']
        matric_no = request.POST['matric_no'].strip().replace('/','-')

        check_d = User.objects.filter(username= matric_no).count()
        check_e = User.objects.filter(email= email).count()
        
        if check_d != 0:
            messages.info(request, 'Username already exists')
            return redirect('register')
        
        if check_e != 0:
            messages.info(request, 'Email already exists')
            return redirect('register')

        user = User.objects.create_user(
            username = matric_no,
            password=password,
            email=email.strip().lower(),
        )
        
        user.save();
        
        userData = UserData.objects.create(
            user=user,
            firstname = firstname,
            lastname = lastname,
            othername = othername,
            level = level,
            dept = dept,
            email = email,
            college = college.upper(),
            matric_no = matric_no,
        )
        
        userData.save();
        messages.info(request, 'User registered Successfully')
        return redirect('login')

    return render(request, 'register.html')
        
        
        

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        
    return redirect('login')