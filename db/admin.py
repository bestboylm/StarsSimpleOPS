from django.contrib import admin
from db import models

# Register your models here.
admin.site.register(models.IDC)
admin.site.register(models.UserInfo)
admin.site.register(models.Server)
admin.site.register(models.Asset)
admin.site.register(models.Business)