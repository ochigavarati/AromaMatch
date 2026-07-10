from flask import Flask
from ext import db
from routes import main

app = Flask(__name__)

app.config["SECRET_KEY"] = "HAUSDUASDASJJIDYAW!@#*!@YBRYAYTYSD123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aromamatch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(main)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)