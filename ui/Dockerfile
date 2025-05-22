# Stage 1: Build
FROM node:20-alpine as builder

WORKDIR /app

# Accept build-time VITE_API_URL
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

COPY ui/package*.json ./
RUN npm install

COPY ui/ ./

RUN VITE_API_URL=$VITE_API_URL npm run build

# Stage 2: Serve with NGINX
FROM nginx:1.25-alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY ui/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]