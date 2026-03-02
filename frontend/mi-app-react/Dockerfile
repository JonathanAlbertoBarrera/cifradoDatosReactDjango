# Dockerfile para React Frontend (Vite)
FROM node:20-alpine AS builder

# Directorio de trabajo
WORKDIR /app

# Copiar package.json y package-lock.json
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar todo el código fuente
COPY . .

# Configurar variable de entorno para Vite
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

# Construir la aplicación para producción
RUN npm run build

# Stage 2: Servir con Nginx
FROM nginx:alpine

# Copiar los archivos construidos desde el stage anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Exponer puerto 80
EXPOSE 80

# Comando por defecto de Nginx
CMD ["nginx", "-g", "daemon off;"]
