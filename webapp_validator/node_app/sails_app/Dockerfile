# Fetching the minified node image on apline linux
FROM node:18-slim

# Declaring env
ENV NODE_ENV development

# Setting up the work directory
WORKDIR /app

# Copying all the files in our project
COPY ./package.json .
COPY ./package-lock.json .

# Installing dependencies
RUN npm install

COPY . .

# Exposing server port
EXPOSE 6000

# Starting our application
CMD [ "node","app.js","--port=6000" ]


