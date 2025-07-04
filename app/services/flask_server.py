from flask import Flask

class FlaskServer:
    def __init__(self, name, config) -> None:
        """
        Initializes the FlaskServer class with the necessary dependencies.
        
        :param name: The name of the Flask application.
        :param config: The configuration object for the Flask application.
        """
        self.app_name = name
        self.env = config
        self.blueprints = []  # List to hold blueprint instances

    def create_app(self):
        """
        Creates and configures the Flask application.
        
        :return: Configured Flask application instance.
        """
        app = Flask(self.app_name)

        # Load environment-specific configurations
        app.config.from_object(self.env)
        # Register blueprints
        self._register_blueprints(app)
        # Setup error handling
        self._setup_error_handlers(app)

        return app

    def add_blueprint(self, blueprint, url_prefix=None):
        """
        Adds a blueprint to the Flask application with an optional URL prefix.

        :param blueprint: The blueprint to register.
        :param url_prefix: (Optional) The URL prefix for the blueprint.
        """
        self.blueprints.append((blueprint, url_prefix))

    def _register_blueprints(self, app):
        """
        Registers all added blueprints to the Flask application with their URL prefixes.

        :param app: The Flask application instance.
        """
        for blueprint, url_prefix in self.blueprints:
            app.register_blueprint(blueprint, url_prefix=url_prefix)

    def _setup_error_handlers(self, app):
        """
        Sets up custom error handlers for the application.
        """
        @app.errorhandler(404)
        def not_found_error(error):
            return {"error": "Resource not found"}, 404

        @app.errorhandler(500)
        def internal_error(error):
            return {"error": "An internal error occurred"}, 500