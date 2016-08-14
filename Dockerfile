FROM cpuskarz/aci-php-nginx
MAINTAINER chet carello "cpuskarz@cisco.com"

EXPOSE 8000
ADD . /app
WORKDIR /app

