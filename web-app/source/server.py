from routes import routes_bp
from backend.usersHandler import users_bp
from backend.devicesHandler import devices_bp

from flask import Flask


app = Flask(__name__)

app.register_blueprint(routes_bp, url_prefix='/')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(devices_bp, url_prefix='/devices')


# 
# Section: RUN
# 

def run():
    app.run(host='0.0.0.0', port=8000)