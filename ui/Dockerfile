# Step 1: Build the React app
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy dependency definitions first (leverage layer caching)
COPY ui/package*.json ./

# Install dependencies
RUN npm ci

# Copy the rest of the frontend source
COPY ui/ .

# Build production-ready static files
RUN npm run build

# Step 2: Serve with NGINX
FROM nginx:stable-alpine

# Copy build output to NGINX's public folder
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 for HTTP traffic
EXPOSE 80

# Start NGINX in foreground
CMD ["nginx", "-g", "daemon off;"]