from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Team, Player, Region
from django.db import IntegrityError

BASE = 'w-full border px-3 py-2 rounded-md'
BASE_INPUT = 'w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-[#0f1b41]'

class TeamForm(forms.ModelForm):
    # field akun user (tidak ada di model)
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': BASE_INPUT}))
    email    = forms.EmailField(widget=forms.EmailInput(attrs={'class': BASE_INPUT}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': BASE_INPUT}))

    def clean_username(self):
        uname = self.cleaned_data['username']
        if User.objects.filter(username__iexact=uname).exists():
            raise ValidationError('Username already taken')
        return uname

    def clean_email(self):
        mail = self.cleaned_data['email']
        if User.objects.filter(email__iexact=mail).exists():
            raise ValidationError('Email already registered')
        return mail

    region   = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        empty_label='Choose Region',
        widget=forms.Select(attrs={'class': BASE_INPUT})
    )
    category = forms.ChoiceField(
        choices=Team.CATEGORY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'flex space-x-4'}),
        required=True
    )

    class Meta:
        model  = Team
        fields = [
            'region', 'school_name', 'school_nickname', 'short_name', 'address',
            'coach_name', 'coach_phone', 'captain_name', 'captain_phone',
            'supporter_name', 'instagram_account', 'achievements',
            'logo', 'team_photo', 'category'
        ]
        widgets = {
            'school_name':      forms.TextInput(attrs={'class': BASE_INPUT}),
            'school_nickname':  forms.TextInput(attrs={'class': BASE_INPUT}),
            'short_name':       forms.TextInput(attrs={'class': BASE_INPUT}),
            'address':          forms.Textarea(attrs={'class': BASE_INPUT, 'rows':3}),
            'coach_name':       forms.TextInput(attrs={'class': BASE_INPUT}),
            'coach_phone':      forms.TextInput(attrs={'class': BASE_INPUT}),
            'captain_name':     forms.TextInput(attrs={'class': BASE_INPUT}),
            'captain_phone':    forms.TextInput(attrs={'class': BASE_INPUT}),
            'supporter_name':   forms.TextInput(attrs={'class': BASE_INPUT}),
            'instagram_account':forms.TextInput(attrs={'class': BASE_INPUT}),
            'achievements':     forms.Textarea(attrs={'class': BASE_INPUT, 'rows':3}),
            'logo':             forms.FileInput(attrs={'class': 'text-sm'}),
            'team_photo':       forms.FileInput(attrs={'class': 'text-sm'}),
        }
    def save(self, commit=True):
        try:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password']
            )
        except IntegrityError:
            # fallback jika tab browser lain submit bersamaan
            raise ValidationError('That username is no longer available, please choose another.')

        team = super().save(commit=False)
        team.user = user
        if commit:
            team.save()
        return team


class PlayerForm(forms.ModelForm):
    position = forms.ChoiceField(
        choices=Player.POSITION_CHOICES,
        widget=forms.Select(attrs={'class': BASE_INPUT})
    )
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class':'text-sm'}))
    supporting_document = forms.FileField(required=False, widget=forms.FileInput(attrs={'class':'text-sm'}))

    class Meta:
        model  = Player
        fields = [
            'name', 'position', 'jersey_number',
            'guardian_name', 'photo', 'supporting_document', 'is_captain'
        ]
        widgets = {
            'name':          forms.TextInput(attrs={'class': BASE_INPUT}),
            'jersey_number': forms.NumberInput(attrs={'class': BASE_INPUT}),
            'guardian_name': forms.TextInput(attrs={'class': BASE_INPUT}),
            'is_captain':    forms.CheckboxInput(attrs={'class':'h-4 w-4 text-[#0f1b41]'}),
        }

class LoginForm(forms.Form):
    identifier = forms.CharField(label='Username or Email',
                                 widget=forms.TextInput(attrs={'class': BASE}))
    password   = forms.CharField(widget=forms.PasswordInput(attrs={'class': BASE}))

    def clean(self):
        data = super().clean()
        from django.contrib.auth.models import User
        ident = data.get('identifier'); pwd = data.get('password')
        try:
            user_obj = User.objects.get(email=ident)
            username = user_obj.username
        except User.DoesNotExist:
            username = ident
        user = authenticate(username=username, password=pwd)
        if not user:
            raise forms.ValidationError('Invalid credentials')
        data['user'] = user; return data


class TeamEditForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=Team.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': BASE}),
        label='Category'
    )

    class Meta:
        model = Team
        exclude = ['user', 'status', 'is_main']
        widgets = {f.name: forms.TextInput(attrs={'class': BASE})
                   for f in model._meta.fields if f.name not in ('id','user','status',
                                                                 'team_photo','logo')}
        widgets.update({
            'address': forms.Textarea(attrs={'class': BASE, 'rows':3}),
        })


class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['team']
        widgets = {f.name: forms.TextInput(attrs={'class': BASE})
                   for f in model._meta.fields if f.name not in
                   ('id','team','photo','supporting_document')}
