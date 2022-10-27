from django.contrib import admin
from .models import Task, Prediction

class TaskAdmin(admin.ModelAdmin):
  readonly_fields = ("created", )

class PredictionAdmin(admin.ModelAdmin):
  readonly_fields = ("created",)

# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(Prediction, PredictionAdmin)
