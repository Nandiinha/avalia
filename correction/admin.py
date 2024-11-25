from django.contrib import admin
from .models import Turma
from .models import Student
from .models import Activity
from .models import Answer
# Register your models here.

admin.site.register(Turma)
admin.site.register(Student)
admin.site.register(Activity)
admin.site.register(Answer)