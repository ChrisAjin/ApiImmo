from django.urls import path
from .views import LoadDatasetView, StatsView, stats_form

urlpatterns =[
    path('stats/', StatsView.as_view(), name='stats'),
    path('load-dataset/', LoadDatasetView.as_view(), name='load-dataset'),
    path('stats-form/', stats_form, name='stats_form'),
]