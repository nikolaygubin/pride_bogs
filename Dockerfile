FROM python:3.9-alpine

# Create app directory
RUN mkdir /app
WORKDIR /app

# Install dependencies
RUN apk add --no-cache python3 postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev \
    && pip install psycopg2-binary==2.9.6 \
    && pip install setuptools==58.2.0

# Clean up build dependencies
#RUN apk --purge del .build-deps

# Copy requirements file and install python requirements
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy the rest of the application
COPY . /app

CMD python /app/telegram_bot.py