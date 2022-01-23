import json, jsonify

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

import raw_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(400))
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String)
    price = db.Column(db.Float)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


db.create_all()

for user_data in raw_data.users:
    new_user = User(
        id=user_data["id"],
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        age=user_data["age"],
        email=user_data["email"],
        role=user_data["role"],
        phone=user_data["phone"],
    )

    db.session.add(new_user)
    db.session.commit()

for order_data in raw_data.orders:
    new_order = Order(
        id=order_data["id"],
        name=order_data["name"],
        description=order_data["description"],
        start_date=order_data["start_date"],
        end_date=order_data["end_date"],
        address=order_data["address"],
        price=order_data["price"],
        customer_id=order_data["customer_id"],
        executor_id=order_data["executor_id"]
    )

    db.session.add(new_order)
    db.session.commit()

for offer_data in raw_data.offers:
    new_offer = Offer(
        id=offer_data["id"],
        order_id=offer_data["order_id"],
        executor_id=offer_data["executor_id"]
    )
    db.session.add(new_offer)
    db.session.commit()


@app.route("/users/", methods=['GET', 'POST', ])
def users():
    if request.method == "GET":
        res = []
        for user in User.query.all():
            res.append(user.to_dict())
        return json.dumps(res), 200
    elif request.method == "POST":
        user_data = json.loads(request.data)
        new_user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"],
        )
        db.session.add(new_user)
        db.session.commit()
        return "", 204


@app.route("/user/<int:id>", methods=['GET', 'POST', 'DELETE'])
def get_user_by_id(id: int):
    if request.method == "GET":
        return json.dumps(User.query.get(id).to_dict()), 200
    elif request.method == "DELETE":
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        user_data = json.loads(request.data)
        user = User.query.get(id)
        user.first_name = user_data["first_name"],
        user.last_name = user_data["last_name"],
        user.age = user_data["age"],
        user.email = user_data["email"],
        user.role = user_data["role"],
        user.phone = user_data["phone"]
        db.session.add(user)
        db.session.commit()
        return "", 204


@app.route("/orders/", methods=['GET', 'POST'])
def orders():
    if request.method == "GET":
        res = []
        for order in Order.query.all():
            res.append(order.to_dict())
        return json.dumps(res, sort_keys=False, indent=4, ensure_ascii=False, ), 200, {
            'Content-Type': 'application/json; charset=utf-8'}
    elif request.method == "POST":
        order_data = json.loads(request.data)
        new_user = Order(
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"]
        )
        db.session.add(new_user)
        db.session.commit()
        return "", 204


@app.route("/order/<int:id>", methods=['GET', 'POST', 'DELETE'])
def get_order_by_id(id: int):
    if request.method == "GET":
        return json.dumps(Order.query.get(id).to_dict(), sort_keys=False, indent=4, ensure_ascii=False, ), 200
    elif request.method == "DELETE":
        get_order = Order.query.get(id)
        db.session.delete(get_order)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        order_data = json.loads(request.data)
        order = Order.query.get(id)
        order.name = order_data["name"],
        order.description = order_data["description"],
        order.start_date = order_data["start_date"],
        order.end_date = order_data["end_date"],
        order.price = order_data["price"],
        order.customer_id = order_data["customer_id"],
        order.executor_id = order_data["executor_id"]
        db.session.add(order)
        db.session.commit()
        return "", 204


@app.route("/offers/", methods=['GET', 'POST'])
def offers():
    if request.method == "GET":
        res = []
        for offer in Offer.query.all():
            res.append(offer.to_dict())
        return json.dumps(res, sort_keys=False, indent=4, ensure_ascii=False, ), 200
    elif request.method == "POST":
        offer_data = json.loads(request.data)
        new_offer = Offer(
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"]
        )
        db.session.add(new_offer)
        db.session.commit()
        return "", 204


@app.route("/offer/<int:id>", methods=['GET', 'POST', 'DELETE'])
def get_offer_by_id(id: int):
    if request.method == "GET":
        return json.dumps(Offer.query.get(id).to_dict(), sort_keys=False, indent=4, ensure_ascii=False, ), 200
    elif request.method == "DELETE":
        get_offer = Offer.query.get(id)
        db.session.delete(get_offer)
        db.session.commit()
        return "", 204
    elif request.method == "PUT":
        offer_data = json.loads(request.data)
        offer = Offer.query.get(id)
        offer.order_id = offer_data["order_id"],
        offer.executor_id = offer_data["executor_id"],
        db.session.add(offer)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run()
