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

# Copy build output to NGINX's public folder
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80 to the world
EXPOSE 80

# Start NGINX in foreground
CMD ["nginx", "-g", "daemon off;"]