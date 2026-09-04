FROM python:3.12-slim

WORKDIR /app

# Install dependencies first so this layer is cached and only rebuilt when
# requirements.txt actually changes - not on every source-code edit.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Application code changes far more often than dependencies, so it's copied
# in last to keep the dependency layer above reusable across builds.
COPY app.py VERSION ./

EXPOSE 5000

CMD ["python", "app.py"]
