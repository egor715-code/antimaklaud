from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, BanTeam, BanReason, Team

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=[(User.Role.MEMBER, 'Обычный пользователь'), (User.Role.ORGANIZER, 'Организатор')], label='Роль')
    phone = forms.CharField(max_length=20, required=True, label='Номер телефона')

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2', 'role']

class BanTeamForm(forms.ModelForm):
    class Meta:
        model = BanTeam
        fields = ['reason', 'ban_date', 'expiry_date', 'description']
        widgets = {
            'ban_date': forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'reason': 'Причина',
            'ban_date': 'Дата бана',
            'expiry_date': 'Дата окончания',
            'description': 'Описание',
        }

class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'messenger_link', 'chevron', 'description']
        labels = {
            'name': 'Название команды',
            'messenger_link': 'Ссылка на мессенджер',
            'chevron': 'Шеврон',
            'description': 'Описание',
        } 