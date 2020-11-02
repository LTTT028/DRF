from django.contrib import admin

# Register your models here.
from demo01 import models

admin.site.register(models.User)
