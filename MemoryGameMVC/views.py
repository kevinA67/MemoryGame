from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import GameResult

def home(request):
    return render(request, 'home.html')

@login_required
def history(request):
    # Mostrar solo partidas del usuario logueado
    results = GameResult.objects.filter(user=request.user).order_by('-played_at')
    return render(request, 'history.html', {'results': results})

@login_required
@csrf_exempt  # Sólo si no usas token CSRF en fetch, si usas token puedes quitar esta línea
def save_result(request):
    if request.method == 'POST':
        won = request.POST.get('won') == 'true'
        score = int(request.POST.get('score', 0))
        result = GameResult(user=request.user, won=won, score=score)
        result.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)
