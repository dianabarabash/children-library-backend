from flask import Flask
from config import Config
from models import db
from resources import api_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(api_bp, url_prefix='/')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
