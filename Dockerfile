FROM python:3.11

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt


RUN pip install -r requirements.txt

ADD . /app

#RUN apt-get update -y
#RUN apt-get install -y python-dev build-essential cmake libsm6 libxext6 libxrender-dev nginx libpcre3 libpcre3-dev
#RUN apt-get install ffmpeg libsm6 libxext6  -y

#COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 5000

RUN usermod -G audio www-data
RUN chown -R www-data:www-data /app && \
    chmod 755 /app

USER www-data
#ENTRYPOINT ["python", "run.py"]
RUN chmod +x ./start.sh
CMD ["./start.sh"]