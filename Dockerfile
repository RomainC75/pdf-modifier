# FROM python:3.10
FROM 3.10-alpine3.17

WORKDIR /app
# EXPOSE 5000

# ENV FLASK_DEBUG 1
# ENV PYTHONUNBUFFERED 0

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

# CMD ["flask", "run", "--host", "0.0.0.0"]
CMD ["python3", "main.py"]

# docker run -p 5000:5000 -v ${PWD}:/app flask-rest-api