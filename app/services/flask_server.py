from flask import Flask

class FlaskServer:
    def __init__(self, name, config) -> None:
        """
        Initialize the FlaskServer with the application name and configuration object.
        
        Parameters:
            name (str): The name to assign to the Flask application instance.
            config: The configuration object containing environment-specific settings.
        """
        self.app_name = name
        self.env = config
        self.blueprints = []  # List to hold blueprint instances

    def create_app(self):
        """
        Create and configure a Flask application with environment settings, registered blueprints, and custom JSON error handlers.
        
        Returns:
            Flask: The fully configured Flask application instance.
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
        Add a Flask blueprint and optional URL prefix for later registration with the application.
        
        Parameters:
        	blueprint: The Flask blueprint to be added.
        	url_prefix: An optional URL prefix to associate with the blueprint routes.
        """
        self.blueprints.append((blueprint, url_prefix))

    def _register_blueprints(self, app):
        """
        Register all stored blueprints with the given Flask application, using their specified URL prefixes if provided.
        
        Parameters:
            app (Flask): The Flask application instance to register blueprints with.
        """
        for blueprint, url_prefix in self.blueprints:
            app.register_blueprint(blueprint, url_prefix=url_prefix)

    def _setup_error_handlers(self, app):
        """
        Set up JSON error handlers for HTTP 404 and 500 errors on the Flask app.
        
        The 404 handler returns a JSON response with an error message for resource not found. The 500 handler returns a JSON response indicating an internal server error.
        """
        @app.errorhandler(404)
        def not_found_error(error):
            """
            Return a JSON response with an error message and HTTP 404 status code when a requested resource is not found.
            
            Returns:
                tuple: A JSON-serializable dictionary containing the error message and the HTTP 404 status code.
            """
            return {"error": "Resource not found"}, 404

        @app.errorhandler(500)
        def internal_error(error):
            """
            Handle HTTP 500 errors by returning a JSON response with an internal server error message.
            
            Returns:
                tuple: A JSON object containing the error message and the HTTP 500 status code.
            """
            return {"error": "An internal error occurred"}, 500