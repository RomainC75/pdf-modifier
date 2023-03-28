# FROM python:3.10
FROM python:3.8-bullseye

WORKDIR /worker

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update && pip install -U  --upgrade pip && apt-get install pip ffmpeg libsm6 libxext6 poppler-utils tesseract-ocr python3-requests -y

COPY requirements.txt .

RUN pip3 install -r requirements.txt

# errors where raised because of redis dependancies, so I tried this way
RUN pip3 install redis rq requests pytest-shutil
RUN pip freeze

RUN pwd
CMD [ "python3", "/worker/app/app.py" ]
