from django.core.exceptions import ValidationError
from django.db import models

class Match(models.Model):
    team_home = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='home_matches')
    team_away = models.ForeignKey('teams.Team', on_delete=models.CASCADE, related_name='away_matches')
    region = models.ForeignKey('teams.Region', on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=[('SMA', 'SMA'), ('KULIAH', 'KULIAH'), ('PROFESIONAL', 'PROFESIONAL')])
    match_date = models.DateTimeField()
    score_home = models.IntegerField(default=0)
    score_away = models.IntegerField(default=0)
    
    def clean(self):
        if self.team_home == self.team_away:
            raise ValidationError("A team cannot play against itself.")

        if self.team_home.category != self.team_away.category:
            raise ValidationError("Teams must be from the same category.")

        if self.team_home.region != self.team_away.region and not (self.team_home.is_representative and self.team_away.is_representative):
            raise ValidationError("Teams must be from the same region unless they are regional representatives.")

    def __str__(self):
        return f"{self.team_home} vs {self.team_away} on {self.match_date}"
