FROM python:3.13

WORKDIR /app



# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    fonts-liberation libappindicator3-1 libasound2 \
    libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 \
    libgdk-pixbuf-2.0-0 libnspr4 libnss3 libx11-6 \
    libxcomposite1 libxdamage1 libxrandr2 xdg-utils \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Add Google Chrome official repo and install
RUN wget -q https://dl.google.com/linux/linux_signing_key.pub -O- \
    | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
    > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copy source code
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir webdriver_manager

CMD ["python3", "main.py"]