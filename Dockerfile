# Use a minimal Python base image
FROM --platform=linux/amd64 python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt .

# Install dependencies without caching wheels
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code and assets
COPY . .

# Explicitly copy soccer_field.jpg in case Docker ignores dotfiles
COPY soccer_field.jpg .

# Expose the port your app listens on
EXPOSE 80

# Run your app
CMD ["python", "app.py"]
