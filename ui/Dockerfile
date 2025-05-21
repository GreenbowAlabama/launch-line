# Step 1: Build the React app
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the frontend code
COPY . .

# Build the production static files
RUN npm run build

# Step 2: Serve with NGINX
FROM nginx:stable-alpine

# Remove default NGINX static files
RUN rm -rf /usr/share/nginx/html/*

# Copy build output from Vite (Vite defaults to /dist)
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start NGINX
CMD ["nginx", "-g", "daemon off;"]