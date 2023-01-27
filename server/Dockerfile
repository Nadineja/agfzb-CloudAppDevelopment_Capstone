# Base image
FROM python:3.8.2

ENV PYTHONBUFFERED 1
ENV PYTHONWRITEBYTECODE 1

# Install and update Python
RUN apt-get update \
    && apt-get install -y netcat

ENV APP=/app

# Switch to App workdir
WORKDIR $APP

# Install requirements
COPY requirements.txt $APP
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the app files
COPY . $APP

# Open the port for Django/Gunicorn
EXPOSE 8000

# Run shell script to start app
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

# Don't forget to start gunicorn server
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangobackend.wsgi"]
