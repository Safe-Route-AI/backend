from flask import Flask
from dotenv import load_dotenv
from src.database.mongo import init_db

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Initialize Database
    with app.app_context():
        init_db()
        
    # Import Blueprints
    from src.api.routes import routes_bp
    from src.api.auth import auth_bp
    from src.api.incidents import incidents_bp
    
    # Register Blueprints
    app.register_blueprint(routes_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(incidents_bp, url_prefix='/api')

    @app.route("/health")
    def health_check():
        return {"status": "healthy"}

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)