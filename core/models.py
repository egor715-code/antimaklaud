from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Администратор'
        ORGANIZER = 'ORGANIZER', 'Организатор'
        MEMBER = 'MEMBER', 'Участник'
    
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.MEMBER,
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    chevron_photo = models.ImageField(upload_to='chevrons/', blank=True, null=True)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.username

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    messenger_link = models.URLField(blank=True, null=True)
    chevron = models.ImageField(upload_to='team_chevrons/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class BanReason(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class BanTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reason = models.ForeignKey(BanReason, on_delete=models.SET_NULL, null=True)
    ban_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Banned Teams"