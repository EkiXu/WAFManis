# Use a slim PHP 7.4 image
FROM php:7.4-fpm

# Set working directory
WORKDIR /var/www/html

# Install system dependencies for Composer
RUN apt-get update && apt-get install -y curl git zip unzip zlib1g-dev libicu-dev g++


RUN docker-php-ext-configure intl
RUN docker-php-ext-install intl

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Copy your project directory
COPY . .

# Accerlate with mirror in China and install composer dependencies
RUN composer config -g repo.packagist composer https://packagist.phpcomposer.com && \
    COMPOSER_ALLOW_SUPERUSER=1 composer install --prefer-dist --no-dev

COPY env .env

EXPOSE 80

# Command to run the application
CMD ["php","spark","serve","--host" ,"0.0.0.0", "--port", "80"]

