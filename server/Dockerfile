from python:alpine3.23

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

RUN apk add --no-cache postgresql-client

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]