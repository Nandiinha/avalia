from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Turma(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.name
            
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    id_class = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='students')
    
class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=1000, null=True, blank=True)
    question = models.CharField(max_length=200, null=True, blank=True)
    id_class = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='activities') 

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    id_activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='answers')
    id_student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answers')
    studentAnswer = models.FileField(upload_to='uploads', null=True, blank=True)
    extract_value = models.CharField(max_length=1000,null=True, blank=True)
    score = models.DecimalField(max_digits=3, decimal_places=1)
    feedback = models.CharField(max_length=1000,null=True, blank=True)
    answer_based = models.BooleanField(null=False)
    teacherAnswer = models.CharField(max_length=1000,null=True, blank=True)
