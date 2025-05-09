FROM python:3.11-slim


WORKDIR /app


RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN pip freeze > installed_apps.txt


EXPOSE 8000


CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
