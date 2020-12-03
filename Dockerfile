FROM python:3.8-slim


# Set work directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt /app/

# Install Requirements
RUN pip install -r requirements.txt

# Copy code
COPY . /app/

CMD gunicorn --workers 10 --bind 0.0.0.0:5000 --log-level DEBUG main:app

