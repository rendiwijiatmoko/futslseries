from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.match_list, name='match_list'),  # Match list page
    path('standings/', views.standings_table, name='standings_table'),  # Standings table page
    path('<int:pk>/', views.match_detail, name='match_detail'),
]
