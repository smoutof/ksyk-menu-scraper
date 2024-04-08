from datetime import datetime
from flask import Flask, jsonify

# Flask App
    
app = Flask(__name__)

@app.route('/')
def index():
    response = jsonify({"url": f"https://www.compass-group.fi/menuapi/week-menus?costCenter=3026&date={datetime.today().strftime('%Y-%m-%d')}&language=fi"})
    response.headers.add('Access-Control-Allow-Origin', '*') 
    return response