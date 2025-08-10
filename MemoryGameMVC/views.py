from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import login, logout
from django.db.models import Avg, Count, Max, Q

from .models import GameResult
from .forms import RegistroForm, LoginForm


# ==============================
# Autenticación
# ==============================
def registro_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ==============================
# Vistas del juego
# ==============================
@login_required
def home(request):
    return render(request, 'home.html')


@login_required
def history(request):
    results = GameResult.objects.filter(user=request.user).order_by('-date_played')
    wins = results.filter(won=True).count()
    losses = results.filter(won=False).count()
    return render(request, 'history.html', {
        'results': results,
        'wins': wins,
        'losses': losses,
    })


@login_required
@require_POST
def save_result(request):
    """
    Guarda resultado de partida.
    Espera POST con: won (true/false), score (int), level (1/2/3), seconds (int)
    """
    won_str = str(request.POST.get('won', '')).lower()
    won = won_str in ('true', '1', 'yes', 'on')

    try:
        score = int(request.POST.get('score', 0) or 0)
    except (TypeError, ValueError):
        score = 0

    try:
        level = int(request.POST.get('level', 1) or 1)
    except (TypeError, ValueError):
        level = 1

    try:
        seconds = int(request.POST.get('seconds', 0) or 0)
    except (TypeError, ValueError):
        seconds = 0

    GameResult.objects.create(
        user=request.user,
        won=won,
        score=score,
        level=level,
        duration_seconds=seconds,
    )
    return JsonResponse({'ok': True})


# ==============================
# Perfil (estadísticas)
# ==============================
@login_required
def profile(request):
    qs = GameResult.objects.filter(user=request.user)

    wins   = qs.filter(won=True).count()
    losses = qs.filter(won=False).count()
    total  = qs.count()

    win_rate  = round((wins / total) * 100, 1) if total else 0.0
    avg_score = qs.aggregate(Avg('score'))['score__avg'] or 0
    avg_time  = qs.aggregate(Avg('duration_seconds'))['duration_seconds__avg'] or 0
    top_score = qs.aggregate(Max('score'))['score__max'] or 0
    last_played = qs.aggregate(Max('date_played'))['date_played__max']

    # Nombres de nivel ACTUALES
    level_row = qs.values('level').annotate(c=Count('id')).order_by('-c').first()
    level_map = {1: 'Básico', 2: 'Medio', 3: 'Avanzado'}
    most_level = level_row['level'] if level_row else None
    most_level_name = level_map.get(most_level, '—') if most_level else '—'

    def mmss(seconds):
        try:
            seconds = int(round(seconds))
        except Exception:
            seconds = 0
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    context = {
        'wins': wins,
        'losses': losses,
        'total': total,
        'win_rate': win_rate,
        'avg_score': int(round(avg_score)) if avg_score else 0,
        'avg_time_str': mmss(avg_time),
        'top_score': top_score,
        'most_level_name': most_level_name,
        'last_played': last_played,
        'recent': qs.order_by('-date_played')[:10],
    }
    return render(request, 'profile.html', context)


# ==============================
# Leaderboard (Top 10)
# ==============================
@login_required
def leaderboard(request):
    stats = (
        GameResult.objects
        .exclude(user__isnull=True)
        .values("user__username")
        .annotate(
            best_score=Max("score"),
            wins=Count("id", filter=Q(won=True)),
            losses=Count("id", filter=Q(won=False)),
            last_played=Max("date_played"),
        )
        .order_by("-best_score", "-wins", "-last_played")[:10]
    )
    return render(request, "leaderboard.html", {"stats": stats})


# ==============================
# Exportar historial a CSV
# ==============================
@login_required
def history_csv(request):
    results = GameResult.objects.filter(user=request.user).order_by('-date_played')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="historial_memoria.csv"'

    import csv
    writer = csv.writer(response)
    writer.writerow(['Fecha', 'Resultado', 'Puntuación', 'Nivel', 'Duración (s)'])

    for r in results:
        writer.writerow([
            r.date_played.strftime("%Y-%m-%d %H:%M:%S"),
            'Ganada' if r.won else 'Perdida',
            r.score,
            r.level,  # si prefieres nombre, puedes mapearlo aquí
            getattr(r, 'duration_seconds', 0),
        ])

    return response
