# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11-slim

# Expose FastAPI default port
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev && apt-get clean

# Install dependencies from requirements.txt
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Set working directory and copy application code
WORKDIR /app
COPY . /app

RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

# enable auto reload for dev
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]