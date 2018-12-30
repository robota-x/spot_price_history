FROM python:3-alpine

COPY requirements.txt ./

# Required to build psycopg2 from source on alpine
RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py" ]