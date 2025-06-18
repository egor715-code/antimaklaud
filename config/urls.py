"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core.views import home, team_detail, teams_banned, register, profile, logout_view, teams_list, ban_team, unban_team, login_view, team_add

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('team/<int:team_id>/', team_detail, name='team_detail'),
    path('teams/banned/', teams_banned, name='teams_banned'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('teams/', teams_list, name='teams_list'),
    path('team/<int:team_id>/ban/', ban_team, name='ban_team'),
    path('team/ban/<int:ban_id>/unban/', unban_team, name='unban_team'),
    path('teams/add/', team_add, name='team_add'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
