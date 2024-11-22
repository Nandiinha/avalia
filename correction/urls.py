from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    #LOGIN
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('plataform/', views.plataform, name='plataform'),

    #HOME
    path('', views.home, name='home'),

    #TURMAS
    path('cursos/', views.cursos, name = "cursos"),
    path('salvar/', views.salvar, name="salvar"),
    path('update/<int:id>', views.update, name="update"),
    path('delete/<int:id>', views.delete, name="delete"),

    #ATIVIDADES
    path('activities/<int:id>/', views.activities, name='activities'),
    path('create_activity/<int:id>/', views.create_activity, name='create_activity'),
    path('select_activity/<int:id>/', views.select_activity, name='select_activity'),
    path('update_activity/<int:id>/', views.update_activity, name='update_activity'),
    path('delete_activity/<int:id>/', views.delete_activity, name='delete_activity'),

    #ANSWERS
    path('activities_details/<int:id>/', views.answers, name='activities_details'),
    path('create_answer/<int:id>/', views.create_answer, name='create_answer'),
    path('select_answer/<int:id>/', views.select_answer, name='select_answer'),
    path('update_correction/<int:id>/', views.update_correction, name='update_correction'),
    path('delete_correction/<int:id>/', views.delete_correction,name='delete_correction'),

    #ALUNOS
    path('students/<int:id>/', views.students, name='students'),
    path('create_student/<int:id>/', views.create_student, name='create_student'),
    path('select_student/<int:id>/', views.select_student, name='select_student'),
    path('update_student/<int:id>', views.update_student, name='update_student'),
    path('delete_student/<int:id>', views.delete_student, name='delete_student'),
    path('studentDetails/<int:id>', views.studentDetails, name='studentDetails'),

    #DETALHES
    path('details/<int:id>/', views.details, name='details'),

    #OCR
   path('extract_text/', views.extract_text, name='extract_text')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)