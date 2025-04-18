# apps/matches/admin.py
from django.contrib import admin
from .models import Match
from .forms import MatchForm

class MatchAdmin(admin.ModelAdmin):
    form = MatchForm

    def get_form(self, request, obj=None, **kwargs):
        # Pass the user context to the form
        kwargs['form'] = MatchForm
        kwargs['form'].user = request.user  # Pass the user to the form
        return super().get_form(request, obj, **kwargs)

admin.site.register(Match, MatchAdmin)
