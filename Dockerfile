FROM python:3.7-alpine as builder
RUN apk update && apk upgrade
RUN apk add gcc python3-dev musl-dev postgresql-dev
COPY bob/src/requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.7-alpine as runner
RUN apk add postgresql-libs
COPY --from=builder /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
COPY . .
WORKDIR /bob
ENTRYPOINT ["python3", "src/start_bot.py"]