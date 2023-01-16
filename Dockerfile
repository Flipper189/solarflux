FROM python:3.10

RUN apt-get update
RUN apt-get -y install cron nano

RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r /app/requirements.txt

COPY solarflux.py /app
RUN chmod 550 /app/solarflux.py

RUN echo "0 * * * * root cd /app && python3 ./solarflux.py > /proc/1/fd/1 2>&1" >> /etc/crontab
CMD ["cron", "-f"]
