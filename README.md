# MemoryGame (Django)

## Requisitos
- Python 3.13
- MySQL 8 (o Docker + docker-compose)

## Configuración
1. Copia `.env.example` a `.env` y ajusta credenciales.
2. Instala dependencias: `pip install -r requirements.txt`
3. Migra: `python manage.py migrate`
4. Ejecuta: `python manage.py runserver`

## Docker (opcional)
`docker compose up --build`

## Funciones
- Juego de memoria (niveles Básico/Medio/Avanzado, intentos y tiempo por nivel).
- Pausar/Reanudar, modal de fin, sonidos, progreso.
- Historial, Perfil (estadísticas), Leaderboard, exportar CSV.
