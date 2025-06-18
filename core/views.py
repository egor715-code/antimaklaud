from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Exists, OuterRef
from django.utils import timezone
from datetime import date
from .models import Team, BanTeam, User
from .forms import UserRegistrationForm, BanTeamForm, TeamForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def team_detail(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return render(request, 'team_detail.html', {'team': team})

def teams_banned(request):
    search_query = request.GET.get('search', '')
    banned_teams = BanTeam.objects.all().order_by('-ban_date')
    if search_query:
        banned_teams = banned_teams.filter(team__name__icontains=search_query)
    return render(request, 'teams_banned.html', {'banned_teams': banned_teams, 'search_query': search_query})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
            user = form.save(commit=False)
            if user.role == User.Role.ORGANIZER:
                user.is_active = False
                user.save()
                messages.info(request, 'Ваша заявка на регистрацию как организатора отправлена. Ожидайте подтверждения администратора.')
                return redirect('login')
            else:
                user.save()
                login(request, user)
                return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required(login_url='/register/')
def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'user': request.user})
    else:
        return render(request, 'profile.html', {'show_login': True})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def teams_list(request):
    search_query = request.GET.get('search', '')
    today = date.today()
    
    # Получаем все активные баны
    active_bans = BanTeam.objects.filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gte=today)
    )
    
    # Получаем ID забаненных команд
    banned_team_ids = active_bans.values_list('team_id', flat=True)
    
    # Базовый запрос для получения команд
    teams = Team.objects.all()
    
    # Исключаем забаненные команды
    if banned_team_ids.exists():
        teams = teams.exclude(id__in=banned_team_ids)
    
    # Применяем поиск, если он есть
    if search_query:
        teams = teams.filter(name__icontains=search_query)
    
    return render(request, 'teams_list.html', {
        'teams': teams,
        'search_query': search_query
    })

def is_organizer(user):
    return user.is_authenticated and user.role == 'ORGANIZER'

@login_required
@user_passes_test(is_organizer)
def ban_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    
    if request.method == 'POST':
        form = BanTeamForm(request.POST)
        if form.is_valid():
            ban = form.save(commit=False)
            ban.team = team
            ban.organizer = request.user
            ban.save()
            messages.success(request, f'Команда {team.name} успешно забанена')
            return redirect('team_detail', team_id=team.id)
    else:
        form = BanTeamForm()
    
    return render(request, 'ban_team.html', {
        'form': form,
        'team': team
    })

@login_required
@user_passes_test(is_organizer)
def unban_team(request, ban_id):
    ban = get_object_or_404(BanTeam, id=ban_id)
    team_name = ban.team.name
    
    if request.method == 'POST':
        ban.delete()
        messages.success(request, f'Команда {team_name} успешно разбанена')
        return redirect('teams_banned')
    
    return render(request, 'unban_team.html', {
        'ban': ban
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'login.html')

@login_required
@user_passes_test(is_organizer)
def team_add(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save()
            return redirect('team_detail', team_id=team.id)
    else:
        form = TeamForm()
    return render(request, 'team_add.html', {'form': form})
