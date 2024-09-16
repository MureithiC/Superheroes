#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes])

# GET /heroes/<int:id>
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dict())

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers])

# GET /powers/<int:id>
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict())

# PATCH /powers/<int:id>
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    if 'description' in data:
        try:
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict()), 200  # Return 200 status code
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 422  # Return 422 status code
    
    return jsonify({"errors": ["Invalid request"]}), 400

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({"errors": ["Strength must be 'Strong', 'Weak', or 'Average'"]}), 422  # Return 422 status code

    try:
        hero_power = HeroPower(
            strength=strength,
            hero_id=data['hero_id'],
            power_id=data['power_id']
        )
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero_power.to_dict()), 201  # Return 201 status code
    except ValueError as e:
        return jsonify({"errors": [str(e)]}), 400
    
if __name__ == '__main__':
    app.run(port=5555, debug=True)