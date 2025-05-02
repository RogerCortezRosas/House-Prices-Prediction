FROM python:3.10-bookworm


WORKDIR /api

COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt

COPY . .


CMD ["uvicorn", "api:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]