# Use a slim PHP 7.4 image
FROM php:7.4-fpm

# Set working directory
WORKDIR /var/www/html

# Install system dependencies for Composer
RUN apt-get update && apt-get install -y curl git zip unzip

# Install Composer
RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer

# Copy your project directory
COPY . .

# Accerlate with mirror in China and install composer dependencies
RUN composer config -g repo.packagist composer https://packagist.phpcomposer.com && \
    COMPOSER_ALLOW_SUPERUSER=1 composer install --prefer-dist --no-dev

COPY .env.example .env

RUN php artisan key:generate

# Expose the port where your Laravel application listens (usually 80)
EXPOSE 80

# Command to run the application
CMD ["php", "artisan","serve" ,"--host" ,"0.0.0.0", "--port", "80"]
