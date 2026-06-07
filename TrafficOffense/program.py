from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Api
from app import traffic_offense_bp


app = Flask(__name__)
api = Api(app)

app.register_blueprint(traffic_offense_bp)

# Define your API routes and controllers here

# Swagger UI setup
SWAGGER_URL = '/api/docs'  # URL for accessing the Swagger UI
API_URL = '/swagger.json'  # URL for the Swagger JSON file

# Create Swagger UI blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "TrafficOffense"
    }
)

# Register the Swagger UI blueprint
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run('0.0.0.0', '80')
