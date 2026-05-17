FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Apply mirror to all pip installs
ENV PIP_INDEX_URL=https://mirror-pypi.runflare.com/simple

WORKDIR /app

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install --no-cache-dir -r requirements.txt

COPY ./core /app/
CMD ["python3","manage.py","runserver","0.0.0.0:8000"]