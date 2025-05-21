# ui/Dockerfile
# Build React app
FROM node:20 AS builder

WORKDIR /app
COPY . .
RUN npm install && npm run build

# Serve static files
FROM nginx:stable-alpine

# Copy build artifacts
COPY --from=builder /app/dist /usr/share/nginx/html

# Ensure custom error routing (e.g., /dashboard)
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]