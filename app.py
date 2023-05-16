from flask import Flask
from flask_cors import CORS
from flask_swagger_generator.components import SwaggerVersion
from flask_swagger_ui import get_swaggerui_blueprint
from flask_swagger_generator.generators import Generator
from src.common.utils import swagger_destination_path, SWAGGER_URL, API_URL
from src.firebase.firebase import initialize_app

initialize_app()

from src.router.api import construct_blueprint_api

generator = Generator.of(SwaggerVersion.VERSION_THREE)


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(construct_blueprint_api(generator))
    generator.generate_swagger(app, destination_path=swagger_destination_path)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={"app_name": "Test application"},  # Swagger UI config overrides
        # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
        #    'clientId': "your-client-id",
        #    'clientSecret': "your-client-secret-if-required",
        #    'realm': "your-realms",
        #    'appName': "your-app-name",
        #    'scopeSeparator': " ",
        #    'additionalQueryStringParams': {'test': "hello"}
        # }
    )

    app.register_blueprint(swaggerui_blueprint)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
