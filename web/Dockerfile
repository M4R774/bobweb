FROM python:3.7-alpine

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python3 web/manage.py makemigrations
RUN python3 web/manage.py migrate
WORKDIR /root/
# TODO: Make entrypoint legit server
ENTRYPOINT ["python3", "web/manage.py", "runserver"]
