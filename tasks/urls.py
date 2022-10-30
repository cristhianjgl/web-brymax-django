from tasks.views import PredictionView
from django.urls import path

urlpatterns = [
  path('predictions/',PredictionView.as_view(),name='prediction_list')
]