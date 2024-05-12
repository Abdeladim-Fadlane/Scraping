FROM debian:11

RUN apt -y update && apt -y upgrade
RUN apt install -y nginx 
RUN apt install -y openssl 

RUN mkdir -p /etc/nginx/ssl 

RUN openssl req -x509 -nodes \
    -keyout /etc/nginx/ssl/private-key.key \
    -out /etc/nginx/ssl/afadlane.42.fr.crt \
    -subj "/" 

COPY nginx.conf /etc/nginx/sites-enabled/default.conf 

CMD [ "nginx", "-g", "daemon off;" ]