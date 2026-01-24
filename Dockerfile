
# Use an official Python runtime as a base image
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client

# Create and activate the virtual environment
RUN python3 -m venv /app/.venv
# RUN source /app/.venv/bin/activate

# Install dependencies
COPY requirements.txt /app/
RUN /app/.venv/bin/pip install -r requirements.txt
# RUN pip install -r requirements.txt

COPY . /app/

# Expose the Django development server port
EXPOSE 8000

# Run the Django development server
CMD ["/app/.venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]