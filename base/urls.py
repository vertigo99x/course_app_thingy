from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login,name='login'),
    path('user/register',views.registerUser,name='register-user'),
    path('logout',views.logout,name='logout'),
    path('',views.dashboard,name='dashboard'),
    path('tasks',views.tasks,name='tasks'),
    path('profile',views.profile,name='profile'),
    path('profile/change-password',views.changePassword,name='change-password'),
    path('course_materials',views.courseMat,name='course-mat'),
    path('course_materials/delete/<str:pk>',views.courseMatDelete,name='mat-delete'),
    path('assignments',views.assignment,name='assignments'),
    path('assignments/update/<str:pk>',views.assignmentUpdate,name='assignment-update'),
    path('assignments/delete/<str:pk>',views.assignmentDelete,name='assignment-delete'),
    path('tasks/update/<str:pk>',views.tasksUpdate,name='tasks-update'),
    path('tasks/delete/<str:pk>',views.tasksDelete,name='tasks-delete'),
]
