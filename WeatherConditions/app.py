import datetime
from flask import Flask, jsonify, render_template, Blueprint, request as flask_request
import random
import time
import re
import json
import jwt

app = Flask(__name__, template_folder='../templates')
weather_conditions_bp = Blueprint('weather_conditions_bp', __name__)

conditionType = [
    "Snowfall", "Rain", "Sunny", "Cloudy"
]

rainSnowIntensity = ["Heavy", "Medium", "Light"]


#regex for postal code validation
pattern = r"^[A-z]\d[A-z]\d[A-z]\d$"

# validating token
SECRET = "my-secret"
def validate_token(token):
    try:
        #decoded = jwt.decode(token_bytes, SECRET, verify=True, algorithms=["HS256"])
        if datetime.datetime.utcnow().timestamp() > token.get("exp"):
            return False
        return True
    except Exception as e:
        print(f'error: {e}')
        return False

@weather_conditions_bp.route('/weatherforecast/<string:postal_code>', methods=['GET'])
def get_weather_forecast(postal_code):
    token = json.loads(flask_request.args.get("token"))
    validated_token = validate_token(token)
    if (validated_token):
        if re.match(pattern, postal_code):
            t = time.localtime(time.time())
            timestamp = f'{t.tm_year}/{t.tm_mon}/{t.tm_mday} - {t.tm_hour}h {t.tm_min}min {t.tm_sec}sec'

            condition = random.choice(conditionType)
            if condition == "Snowfall" or condition == "Rain" :
                intensity = random.choice(rainSnowIntensity)
                weather_forecast = {
                    'Postal_Code' : postal_code,
                    'Temperature': random.randint(-40, 40),
                    'Conditions': {
                        "type": condition, 
                        "intensity": intensity
                    },
                    'Date': timestamp
                }
            else:
                intensity = "n/a"
                weather_forecast = {
                    'Postal_Code' : postal_code,
                    'Temperature': random.randint(-40, 40),
                    'Conditions': {
                        "type": condition, 
                        "intensity": intensity
                    },
                    'Date': timestamp
                }

            return weather_forecast
            #return render_template('dashboard.html', weather_data=weather_forecast)
        return jsonify({'status code': 400, 'message': 'Invalid postal code'})
    return jsonify({'status code': 401, 'message': 'Invalid token'})