from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import TeamForm, PlayerForm, TeamEditForm, LoginForm
from .models import Team, Player
from .utils import team_owner_required


# ---------- PUBLIC ----------
def list_teams(request):
    teams = Team.objects.filter(status='approved')
    page_obj = Paginator(teams, 12).get_page(request.GET.get('page'))
    return render(request, 'teams/list_teams.html', {'page_obj': page_obj})


def team_detail(request, slug):
    team = get_object_or_404(Team, slug=slug, status='approved')
    players = team.players.all().order_by('-is_captain', 'name')
    return render(request, 'teams/team_detail.html',
                  {'team': team, 'players': players})


def register_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save()
            messages.success(request, "Team registered successfully. Now add players.")
            return redirect('add_players', team_id=team.id)
        messages.error(request, "Please fix the errors below.")
    else:
        form = TeamForm()
    return render(request, 'teams/register_team.html', {'team_form': form})


@team_owner_required
def add_players(request, team_id):
    team = request.team            # di‐set oleh decorator
    form = PlayerForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        player = form.save(commit=False)
        player.team = team
        player.save()
        return redirect('add_players', team_id=team.id)

    return render(request, 'teams/add_players.html',
                  {'team': team, 'player_form': form, 'players': team.players.all()})


def payment(request):
    return render(request, 'teams/payment.html')


# ---------- AUTH ----------
def team_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.cleaned_data['user'])
        return redirect('dashboard')
    return render(request, 'teams/login.html', {'form': form})


def team_logout(request):
    logout(request)
    return redirect('home')


# ---------- DASHBOARD (OWNER) ----------
@login_required
def dashboard(request):
    team = get_object_or_404(Team, user=request.user)
    form = TeamEditForm(request.POST or None, request.FILES or None, instance=team)
    if request.method == 'POST' and form.is_valid():
        form.save(); return redirect('dashboard')
    return render(request, 'teams/dashboard.html',
                  {'team': team, 'form': form, 'players': team.players.all()})


@login_required
def player_add(request):
    team = get_object_or_404(Team, user=request.user)
    form = PlayerForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        p = form.save(commit=False); p.team = team; p.save()
        return redirect('dashboard')
    return render(request, 'teams/player_form.html', {'form': form, 'title': 'Add Player'})


@login_required
def player_edit(request, pk):
    team = get_object_or_404(Team, user=request.user)
    player = get_object_or_404(Player, pk=pk, team=team)
    form = PlayerForm(request.POST or None, request.FILES or None, instance=player)
    if request.method == 'POST' and form.is_valid():
        form.save(); return redirect('dashboard')
    return render(request, 'teams/player_form.html', {'form': form, 'title': 'Edit Player'})


@login_required
def player_delete(request, pk):
    team = get_object_or_404(Team, user=request.user)
    player = get_object_or_404(Player, pk=pk, team=team)
    if request.method == 'POST':
        player.delete(); return redirect('dashboard')
    return render(request, 'teams/player_confirm_delete.html', {'player': player})


def player_list(request):
    # select_related atau prefetch_related untuk optimasi
    players = Player.objects.select_related('team').all()
    return render(request, 'teams/player_list.html', {'players': players})

def player_detail(request, pk):
    player = get_object_or_404(Player.objects.select_related('team'), pk=pk)
    return render(request, 'teams/player_detail.html', {'player': player})