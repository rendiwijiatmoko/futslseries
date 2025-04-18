# apps/matches/views.py
from django.shortcuts import render, get_object_or_404
from .models import Match

def match_list(request):
    # Ambil semua pertandingan
    matches = Match.objects.all().order_by('-match_date')  # Urutkan berdasarkan tanggal pertandingan
    return render(request, 'matches/match_list.html', {'matches': matches})
def match_detail(request, pk):
    # Ambil pertandingan atau 404 jika tidak ada
    match = get_object_or_404(Match, pk=pk)
    return render(request, 'matches/match_detail.html', {
        'match': match,
    })

def standings_table(request):
    teams = {}

    # Ambil semua pertandingan
    matches = Match.objects.all()

    for match in matches:
        # Hitung hasil untuk home team dan away team
        home_points = 0
        away_points = 0
        home_goals = match.score_home
        away_goals = match.score_away

        # Tentukan poin berdasarkan hasil pertandingan
        if home_goals > away_goals:
            home_points = 3  # Home team wins
            away_points = 0  # Away team loses
        elif home_goals < away_goals:
            home_points = 0  # Home team loses
            away_points = 3  # Away team wins
        else:
            home_points = 1  # Draw
            away_points = 1  # Draw

        # Update statistik untuk team_home
        if match.team_home.id not in teams:
            teams[match.team_home.id] = {
                'team': match.team_home,
                'matches_played': 0,
                'wins': 0,
                'draws': 0,
                'losses': 0,
                'goals_for': 0,
                'goals_against': 0,
                'goal_difference': 0,
                'points': 0
            }
        teams[match.team_home.id]['matches_played'] += 1
        teams[match.team_home.id]['goals_for'] += home_goals
        teams[match.team_home.id]['goals_against'] += away_goals
        teams[match.team_home.id]['goal_difference'] += home_goals - away_goals
        teams[match.team_home.id]['points'] += home_points

        # Update statistik untuk team_away
        if match.team_away.id not in teams:
            teams[match.team_away.id] = {
                'team': match.team_away,
                'matches_played': 0,
                'wins': 0,
                'draws': 0,
                'losses': 0,
                'goals_for': 0,
                'goals_against': 0,
                'goal_difference': 0,
                'points': 0
            }
        teams[match.team_away.id]['matches_played'] += 1
        teams[match.team_away.id]['goals_for'] += away_goals
        teams[match.team_away.id]['goals_against'] += home_goals
        teams[match.team_away.id]['goal_difference'] += away_goals - home_goals
        teams[match.team_away.id]['points'] += away_points

        # Update win, draw, and loss counts
        if home_points == 3:
            teams[match.team_home.id]['wins'] += 1
            teams[match.team_away.id]['losses'] += 1
        elif away_points == 3:
            teams[match.team_away.id]['wins'] += 1
            teams[match.team_home.id]['losses'] += 1
        else:
            teams[match.team_home.id]['draws'] += 1
            teams[match.team_away.id]['draws'] += 1

    # Urutkan tim berdasarkan poin
    sorted_teams = sorted(teams.values(), key=lambda x: x['points'], reverse=True)

    return render(request, 'matches/standings_table.html', {'standings': sorted_teams})
