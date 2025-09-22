FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

# Install Dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Upgrade pip
RUN pip install --upgrade pip

COPY . .