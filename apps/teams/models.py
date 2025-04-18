from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.utils.text import slugify 


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Team(models.Model):
    CATEGORY_CHOICES = [
        ('sma',        'SMA'),
        ('kuliah',     'Kuliah'),
        ('profesional','Profesional'),
    ]
    STATUS_CHOICES = [
        ('approved',   'Approved'),
        ('rejected',   'Rejected'),
        ('whitelist',  'Whitelist'),
        ('pending',    'Pending'),
    ]

    # hubungan & info dasar
    user              = models.OneToOneField(User, on_delete=models.CASCADE)
    region            = models.ForeignKey(Region, on_delete=models.CASCADE)
    school_name       = models.CharField(max_length=255)
    school_nickname   = models.CharField(max_length=100)
    short_name        = models.CharField(
        max_length=8, blank=True,
        help_text='Singkatan 3‑8 huruf, mis. FCB, BVB')
    address           = models.TextField()
    slug            = models.SlugField(unique=True, blank=True)

    # staf
    coach_name        = models.CharField(max_length=100)
    coach_phone       = models.CharField(max_length=15)
    captain_name      = models.CharField(max_length=100)
    captain_phone     = models.CharField(max_length=15)

    # lain‑lain
    supporter_name    = models.CharField(max_length=100)
    instagram_account = models.CharField(max_length=100, blank=True)
    achievements      = models.TextField()

    # media
    logo        = models.ImageField(upload_to='team_logos/',  blank=True, null=True)
    team_photo  = models.ImageField(upload_to='team_photos/')

    category    = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='sma')
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    is_main = models.BooleanField(default=False, help_text="Tick for 12 flagship clubs")
    slug = models.SlugField(max_length=60, unique=True, blank=True, null=True)


    def __str__(self):
        return self.school_name
    
    def save(self, *args, **kwargs):
        # generate slug unik jika belum ada
        if not self.slug:
            base = slugify(self.school_name) or "team"
            slug = base
            i = 1
            while Team.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug[:60]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('team_detail', kwargs={'slug': self.slug})

    # helper — mudah dipakai di template
    @property
    def logo_url(self):
        return self.logo.url if self.logo else ''


class Player(models.Model):
    POSITION_CHOICES = [
        ('kiper',  'Kiper'),
        ('anchor', 'Anchor'),
        ('flank',  'Flank'),
        ('pivot',  'Pivot'),
    ]

    team                = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name                = models.CharField(max_length=100)
    position            = models.CharField(max_length=20, choices=POSITION_CHOICES)
    jersey_number       = models.CharField(max_length=3)
    guardian_name       = models.CharField(max_length=100)
    photo               = models.ImageField(upload_to='player_photos/', blank=True, null=True)
    supporting_document = models.FileField(upload_to='supporting_documents/', blank=True, null=True)
    is_captain          = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class TeamEditForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ['user', 'status', 'is_main', ]
        widgets = {f.name: forms.TextInput(attrs={
                     'class': 'w-full border px-3 py-2 rounded-md'})
                   for f in model._meta.fields if f.name not in ['id', 'user', 'status', 'team_photo', 'logo']}

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['team']
        widgets = {f.name: forms.TextInput(attrs={
                     'class': 'w-full border px-3 py-2 rounded-md'})
                   for f in model._meta.fields if f.name not in ['id','team','photo','supporting_document']}
