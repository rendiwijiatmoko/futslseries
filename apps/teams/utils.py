# apps/teams/utils.py
from django.http import HttpResponseForbidden
from .models import Team

def team_owner_required(view_func):
    """
    Pastikan user login & memang pemilik tim.
    dipakai pada view add_players, player_edit, dll.
    """
    def _wrapped(request, team_id=None, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('login')
        team = Team.objects.filter(user=request.user).first()
        if not team or (team_id and team.id != int(team_id)):
            return HttpResponseForbidden('Not allowed')
        # masukkan tim ke request biar view enak
        request.team = team
        return view_func(request, *args, **kwargs)
    return _wrapped
