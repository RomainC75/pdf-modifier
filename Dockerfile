# FROM python:3.10
FROM python:3.8-bullseye

WORKDIR /app

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
RUN pwd
CMD ["python3", "/app/main.py"]
