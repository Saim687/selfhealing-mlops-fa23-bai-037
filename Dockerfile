FROM python:3.9-slim
WORKDIR /app

# Install system utilities and fetch the direct Chrome binary package
RUN apt-get update && apt-get install -y wget unzip curl \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \ 
    && rm google-chrome-stable_current_amd64.deb \
    && apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
