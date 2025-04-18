from django.db import models
from apps.teams.models import Team


class VideoHighlight(models.Model):
    title       = models.CharField(max_length=150)
    youtube_url = models.URLField()
    is_active   = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Highlight Video'
        verbose_name_plural = 'Highlight Videos'

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        """
        Convert normal YouTube URL to embeddable format.
        https://youtu.be/abc -> https://www.youtube.com/embed/abc
        """
        import re
        match = re.search(r'(?:v=|be/)([\w-]{11})', self.youtube_url)
        return f"https://www.youtube.com/embed/{match.group(1)}" if match else ""


class Partner(models.Model):
    name  = models.CharField(max_length=100)
    logo  = models.ImageField(upload_to='partners/')
    url   = models.URLField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class SuccessStory(models.Model):
    title   = models.CharField(max_length=150)
    image   = models.ImageField(upload_to='success_stories/')
    summary = models.TextField(max_length=300)
    link    = models.URLField(blank=True)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
