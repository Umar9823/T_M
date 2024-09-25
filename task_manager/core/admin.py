from django.contrib import admin
from .models import User, Task, Department, Role

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Department)
admin.site.register(Role)
