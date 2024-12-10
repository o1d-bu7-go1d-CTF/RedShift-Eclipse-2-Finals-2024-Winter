# Use an official PHP image with Apache
FROM php:8.2-apache

# Install necessary dependencies and PHP extensions
RUN apt-get update && apt-get install -y \
    libicu-dev \
    libxml2-dev \
    libpq-dev \
    git \
    unzip

# Install PHP extensions
RUN docker-php-ext-install pdo pdo_mysql

# Enable Apache mod_rewrite
RUN a2enmod rewrite

# Set working directory to /var/www/html
WORKDIR /var/www/html

# Copy the PHP source code into the container
COPY ./public /var/www/html/public
COPY ./sql /var/www/html/sql
COPY ./templates /var/www/html/templates
COPY ./static /var/www/html/static
COPY ./vendor /var/www/html/vendor

# Set public directory as the root for the website
RUN sed -i 's|DocumentRoot /var/www/html|DocumentRoot /var/www/html/public|' /etc/apache2/sites-available/000-default.conf

# Add Alias directive to Apache configuration
RUN echo 'Alias /static /var/www/html/static' >> /etc/apache2/sites-available/000-default.conf

# Set appropriate permissions for Apache
RUN chown -R www-data:www-data /var/www/html/ \
    && chmod -R 755 /var/www/html/

# Expose port 80 for Apache
EXPOSE 80
