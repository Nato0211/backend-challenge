from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:renato@localhost/challengecredigob'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    with app.app_context():
        db.create_all() 
        

    from .routes import main
    app.register_blueprint(main)

    return app