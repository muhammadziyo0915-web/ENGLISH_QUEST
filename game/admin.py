from django.contrib import admin
from .models import Stage, Question, Progress, Profile, Inventory

admin.site.register(Stage)
admin.site.register(Question)
admin.site.register(Progress)
admin.site.register(Profile)
admin.site.register(Inventory)
