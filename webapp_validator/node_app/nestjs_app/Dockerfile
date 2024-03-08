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

# Starting our application
CMD [ "npm", "run","start" ]

# Exposing server port
EXPOSE 6000
