FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
VOLUME /app
WORKDIR /app
RUN pip3 install flask
ENTRYPOINT ["python3"]
CMD ["app.py"]