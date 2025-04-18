# apps/matches/forms.py
from django import forms
from .models import Match

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Safely get the user if it's provided, otherwise set it to None
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only allow admin to add matches
        if self.user and not self.user.is_superuser:
            raise forms.ValidationError("You do not have permission to add matches.")
