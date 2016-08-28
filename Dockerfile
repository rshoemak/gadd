FROM cpuskarz/gadd:1
MAINTAINER chet carello "cpuskarz@cisco.com"

EXPOSE 8000
ADD . /app

# use the following workdir for non-php demo
# WORKDIR /app/ui

# use this workdir for php flow
WORKDIR /app/ui/gophp

CMD ["php", "-S", "0.0.0.0:8000"]
