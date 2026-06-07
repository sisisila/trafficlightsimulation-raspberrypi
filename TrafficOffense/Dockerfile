# Use the official Python image from Docker Hub
FROM python:3.8-slim-buster
WORKDIR /app
EXPOSE 80
COPY ./TrafficOffense/requirements.txt /app
COPY ./TrafficOffense/app.py ./TrafficOffense/program.py ./TrafficOffense/trafficoffense.py /app/
RUN pip install -r requirements.txt
RUN export FLASK_APP=program.py
ENTRYPOINT [ "python3", "program.py"]
