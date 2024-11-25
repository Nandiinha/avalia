from django.contrib import admin

from .models import Activity, Answer, Student, Turma

# Register your models here.

admin.site.register(Turma)
admin.site.register(Student)
admin.site.register(Activity)
admin.site.register(Answer)
