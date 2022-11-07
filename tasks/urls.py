from tasks.views import PredictionView, AccesoView
from django.urls import path

urlpatterns = [
  path('predictions/',PredictionView.as_view(),name='prediction_list'),
  path('acceso/',AccesoView.as_view(),name='acceso')
]