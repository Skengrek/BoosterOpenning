FROM node:14-buster-slim

# Install NGINX
RUN apt-get update && apt-get install -y nginx

# Create the directory for NGINX if it doesn't exist
RUN mkdir -p /usr/share/nginx/html

# Remove existing node_modules (if any)
RUN rm -rf node_modules

# Make the 'app' folder the current working directory
WORKDIR /app

# Copy 'package.json' and 'package-lock.json'
COPY package*.json ./

# Install project dependencies
RUN npm set strict-ssl false && npm install

# Copy project files
COPY ./ ./

# Build app for production
RUN npm run build

# Copy custom NGINX configuration (if you have one)
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start NGINX server
CMD ["nginx", "-g", "daemon off;"]