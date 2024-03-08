# Use an official PHP runtime as a parent image
FROM php:7.4-apache

# Set the working directory in the container
WORKDIR /var/www/html

# Install system dependencies for Composer
RUN apt-get update && apt-get install -y curl git zip unzip

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Copy your project directory
COPY . .

# Install composer dependencies and accerlate with mirror in China
RUN composer config -g repo.packagist composer https://packagist.phpcomposer.com && \
    COMPOSER_ALLOW_SUPERUSER=1 composer install --prefer-dist --no-dev

# Expose the port where your Laravel application listens (usually 80)
EXPOSE 80

# Command to run the application
CMD ["php", "-S", "0.0.0.0:80", "-t", "public"]
