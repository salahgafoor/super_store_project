from django.contrib import admin
from accounts import models

admin.site.register(models.UserProfileInfo)
admin.site.register(models.Product)
admin.site.register(models.Order)