FROM python:3-slim-stretch
USER root
WORKDIR /root/
COPY . .
RUN pip install -r requirements.txt
# cd to ensure that db_file is in the right location
WORKDIR /root/web/
RUN python3 manage.py migrate
WORKDIR /root/
ENTRYPOINT ["python3", "web/manage.py", "runserver"]