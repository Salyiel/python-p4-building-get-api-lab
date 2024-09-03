#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def index():
    return "Index for Bakery/BakedGood API"

# Get all bakeries
@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_list = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        jsonify(bakeries_list),
        200,
        {"Content-Type": "application/json"}
    )

    return response

# Get a single bakery by id with its baked goods nested
@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # Retrieve the bakery with the given ID
    bakery = Bakery.query.filter(Bakery.id == id).first()

    # Check if the bakery exists
    if bakery:
        # Convert the bakery object to a dictionary
        bakery_dict = bakery.to_dict()

        # Create a response with the bakery dictionary and a 200 status code
        response = make_response(bakery_dict, 200)
    else:
        # If the bakery is not found, return an error message with a 404 status code
        response = make_response(
            jsonify({"error": "Bakery not found"}),
            404
        )

    return response

# Get all baked goods sorted by price in descending order
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = [baked_good.to_dict() for baked_good in baked_goods]

    response = make_response(
        jsonify(baked_goods_list),
        200,
        {"Content-Type": "application/json"}
    )

    return response

# Get the most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if baked_good:
        baked_good_dict = baked_good.to_dict()
        response = make_response(
            jsonify(baked_good_dict),
            200
        )
    else:
        response = make_response(
            jsonify({"error": "No baked goods found"}),
            404
        )

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)