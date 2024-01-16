FROM node:14-buster-slim

# Remove existing node_modules
RUN rm -rf node_modules

RUN apt-get update \
    # Translations dependencies
    && apt-get install -y gettext \
    && apt-get install -y ca-certificates

# make the 'app' folder the current working directory
WORKDIR /app

# copy both 'package.json' and 'package-lock.json' (if available)
COPY package*.json ./

RUN npm set strict-ssl false
# install project dependencies
RUN npm install

# Remove existing node_modules
RUN rm -rf node_modules

# copy project files and folders to the current working directory (i.e. 'app' folder)
COPY ./ ./

# build app for production with minification
RUN npm run build