FROM node:20-alpine AS builder
WORKDIR /app

COPY web/package*.json ./
RUN npm ci || true

COPY web/ .
RUN npm run build || true

FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


