import json

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import main

app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route("/users/", methods=['GET', 'POST', ])
def users():
    if request.method == "GET":
        res = []
        for user in main.User.query.all():
            res.append(user.to_dict())
        return json.dumps(res), 200
    elif request.method == "POST":
        user_data = json.load(request.data)
        new_user = main.User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        main.db.session.add(new_user)
        main.db.session.commit()
        return "", 204


@app.route("/user/<int:id>", methods=['GET', 'POST', 'DELETE'])
def get_user_by_id(id: int):
    if request.method == "GET":
        return json.dumps(main.User.query.get(id).to_dict()), 200
    elif request.method == "DELETE":
        user = main.User.query.get(id)
        main.db.session.delete(user)
        main.db.session.commit()
        return "", 204
    elif request.method == "PUT":
        user_data = json.loads(request.data)
        user = main.User.query.get(id)
        user.first_name = user_data["first_name"],
        user.last_name = user_data["last_name"],
        user.age = user_data["age"],
        user.email = user_data["email"],
        user.role = user_data["role"],
        user.phone = user_data["phone"]
        main.db.session.add(user)
        main.db.session.commit()
        return "", 204


@app.route("/orders/", methods=['GET', 'POST'])
def orders():
    if request.method == "GET":
        res = []
        for order in main.Order.query.all():
            res.append(order.to_dict())
        return json.dumps(res, sort_keys=False, indent=4, ensure_ascii=False, ), 200, {
            'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        order_data = json.load(request.data)
        new_user = main.Order(
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"]
        )
        main.db.session.add(new_user)
        main.db.session.commit()
        return "", 204


@app.route("/order/<int:id>", methods=['GET', 'POST', 'DELETE'])
def get_order_by_id(id: int):
    if request.method == "GET":
        return json.dumps(main.Order.query.get(id).to_dict(), sort_keys=False, indent=4, ensure_ascii=False, ), 200
    elif request.method == "DELETE":
        get_order = main.Order.query.get(id)
        main.db.session.delete(get_order)
        main.db.session.commit()
        return "", 204
    elif request.method == "PUT":
        order_data = json.loads(request.data)
        order = main.Order.query.get(id)
        order.name = order_data["name"],
        order.description = order_data["description"],
        order.start_date = order_data["start_date"],
        order.end_date = order_data["end_date"],
        order.price = order_data["price"],
        order.customer_id = order_data["customer_id"],
        order.executor_id = order_data["executor_id"]
        main.db.session.add(order)
        main.db.session.commit()
        return "", 204


@app.route("/offers/", methods=['GET', 'POST'])
def offers():
    if request.method == "GET":
        res = []
        for offer in main.Offer.query.all():
            res.append(offer.to_dict())
        return json.dumps(res, sort_keys=False, indent=4, ensure_ascii=False, ), 200
    elif request.method == "POST":
        offer_data = json.load(request.data)
        new_offer = main.Offer(
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"]
        )
        main.db.session.add(new_offer)
        main.db.session.commit()
        return "", 204


@app.route("/offer/<int:id>", methods=['GET', 'POST', 'DELETE'])
def get_offer_by_id(id: int):
    if request.method == "GET":
        return json.dumps(main.Offer.query.get(id).to_dict(), sort_keys=False, indent=4, ensure_ascii=False, ), 200
    elif request.method == "DELETE":
        get_offer = main.Offer.query.get(id)
        main.db.session.delete(get_offer)
        main.db.session.commit()
        return "", 204
    elif request.method == "PUT":
        offer_data = json.loads(request.data)
        offer = main.Offer.query.get(id)
        offer.order_id = offer_data["order_id"],
        offer.executor_id = offer_data["executor_id"],
        main.db.session.add(offer)
        main.db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
