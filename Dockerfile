FROM python:3.12.6-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    build-essential \
    pkg-config \
    netcat-openbsd \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get remove -y gcc build-essential \
    && apt-get autoremove -y \
    && apt-get clean

COPY . .

RUN chmod +x wait-for-db.sh

EXPOSE 8000

CMD ["./wait-for-db.sh", "python", "manage.py", "runserver", "0.0.0.0:8000"]

