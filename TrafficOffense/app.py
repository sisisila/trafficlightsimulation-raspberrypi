# Sila Ben Khelifa
# 2135666
# Sept. 26th, 2023

import datetime
from flask import Flask, jsonify, render_template, Blueprint, request as flask_request
import json
import random
import time
import re

app = Flask(__name__, template_folder='../templates')
traffic_offense_bp = Blueprint('traffic_offense_bp', __name__)

detections = [
    "motion", "collision"
]
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


@traffic_offense_bp.route('/trafficoffense/<string:postal_code>', methods=['GET'])
def get_traffic_offense(postal_code):
    token = json.loads(flask_request.args.get("token"))
    validated_token = validate_token(token)
    if (validated_token):
        if re.match(pattern, postal_code):
            t = time.localtime(time.time())
            timestamp = f'{t.tm_year}/{t.tm_mon}/{t.tm_mday} - {t.tm_hour}h {t.tm_min}min {t.tm_sec}sec'
            traffic_offense = {
                'Postal_Code': postal_code,
                'Detection': {"type": random.choice(detections), "value": bool(random.getrandbits(1))},
                'Date': timestamp
            }

            return traffic_offense
            #return render_template('dashboard.html', traffic_data=traffic_offense)
        return jsonify({'statuscode': 400, 'message': 'Invalid postal code'})
    return jsonify({'status code': 401, 'message': 'Invalid token'})

