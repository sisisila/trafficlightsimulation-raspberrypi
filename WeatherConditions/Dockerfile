FROM python:3.8-slim-buster
WORKDIR /app
EXPOSE 80
COPY ./WeatherConditions/requirements.txt /app
COPY ./WeatherConditions/app.py ./WeatherConditions/program.py ./WeatherConditions/weatherconditions.py /app/
RUN pip install -r requirements.txt
RUN export FLASK_APP=program.py
CMD [ "python3", "program.py"]
