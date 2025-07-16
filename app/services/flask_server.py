from flask import Flask

class FlaskServer:
    def __init__(self, name, config) -> None:
        """
        Initialize a FlaskServer instance with the application name and configuration.
        
        Parameters:
            name (str): The name of the Flask application.
            config: The configuration object used to set up the Flask application.
        """
        self.app_name = name
        self.env = config
        self.blueprints = []  # List to hold blueprint instances

    def create_app(self):
        """
        Create and configure a Flask application instance with loaded environment settings, registered blueprints, and custom error handlers.
        
        Returns:
            Flask: The configured Flask application instance.
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
        Adds a blueprint and optional URL prefix to be registered with the Flask application.
        
        Parameters:
        	blueprint: The Flask blueprint to add.
        	url_prefix: Optional URL prefix to associate with the blueprint.
        """
        self.blueprints.append((blueprint, url_prefix))

    def _register_blueprints(self, app):
        """
        Register all stored blueprints with the Flask application, applying their associated URL prefixes.
        """
        for blueprint, url_prefix in self.blueprints:
            app.register_blueprint(blueprint, url_prefix=url_prefix)

    def _setup_error_handlers(self, app):
        """
        Configure the Flask app to return JSON responses for 404 and 500 HTTP errors.
        
        The 404 handler returns a JSON message indicating the resource was not found. The 500 handler returns a JSON message indicating an internal server error.
        """
        @app.errorhandler(404)
        def not_found_error(error):
            """
            Return a JSON response indicating a 404 Not Found error.
            
            Returns:
                tuple: A dictionary with an error message and the HTTP 404 status code.
            """
            return {"error": "Resource not found"}, 404

        @app.errorhandler(500)
        def internal_error(error):
            """
            Handle HTTP 500 errors by returning a JSON response indicating an internal server error.
            
            Returns:
            	A tuple containing a JSON error message and the HTTP 500 status code.
            """
            return {"error": "An internal error occurred"}, 500