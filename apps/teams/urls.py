from django.urls import path
from . import views

urlpatterns = [
    # auth
    path('login/',  views.team_login,  name='login'),
    path('logout/', views.team_logout, name='logout'),

    # dashboard & players
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/player/add/',              views.player_add,    name='player_add'),
    path('dashboard/player/<int:pk>/edit/',    views.player_edit,   name='player_edit'),
    path('dashboard/player/<int:pk>/delete/',  views.player_delete, name='player_delete'),

    # publik
    path('list/',                   views.list_teams,   name='list_teams'),
    path('register/',               views.register_team, name='register'),
    path('add_players/<int:team_id>/', views.add_players, name='add_players'),
    path('payment/',                views.payment,      name='payment'),

    # players
    path('players/', views.player_list, name='player_list'),
    path('players/<int:pk>/', views.player_detail, name='player_detail'),

    # detail tim  ── letakkan PALING BAWAH agar tidak men‑capt ure route lain
    path('<slug:slug>/',            views.team_detail,  name='team_detail'),
]
