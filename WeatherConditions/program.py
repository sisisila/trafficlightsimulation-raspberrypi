from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Api
from app import weather_conditions_bp


app = Flask(__name__)
api = Api(app)

app.register_blueprint(weather_conditions_bp)

SWAGGER_URL = '/api/docs'  # URL for accessing the Swagger UI
API_URL = '/swagger.json'  # URL for the Swagger JSON file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "weatherConditions"
    }
)

app.register_blueprint(swagger_ui_blueprint)
# app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


if __name__ == '__main__':
    app.run('0.0.0.0', '80')

