FROM ubuntu:latest
RUN apt update && apt install -y python sysstat iproute2 uwsgi uwsgi-plugin-python nginx && apt clean cache
RUN mkdir /files && chown 33:33 /files && chmod 6755 /files
COPY $PWD/configs/site_nginx.conf /etc/nginx/sites-enabled/default
COPY $PWD/configs/site_uwsgi.ini /etc/uwsgi.ini

# CMD ["service uwsgi start", "service nginx start"]

#ENTRYPOINT ["python /files/app.py"]
#ENTRYPOINT ["/bin/bash -c 'python /files/app.py'"]
