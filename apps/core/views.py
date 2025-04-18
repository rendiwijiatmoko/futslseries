from django.shortcuts import render
from django.utils import timezone
from apps.matches.models import Match
from apps.teams.models   import Team
from .models     import VideoHighlight, Partner, SuccessStory

def home(request):
    today = timezone.localdate()

    upcoming = (Match.objects
                .filter(match_date__gte=today)
                .order_by('match_date')[:10])

    highlight = VideoHighlight.objects.filter(is_active=True).first()
    partners  = Partner.objects.all()
    main_clubs = Team.objects.filter(is_main=True)[:12]
    stories  = SuccessStory.objects.all()[:3]

    return render(request, 'core/home.html', {
        'upcoming_matches': upcoming,
        'highlight': highlight,
        'partners': partners,
        'main_clubs': main_clubs,
        'stories': stories,
    })
