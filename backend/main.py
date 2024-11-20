# localhost:5000/create_contact      #endpoint
#
# Request
# type--
# GET         retrieve something
# POST         create something new
# PUT/PATCH    to update something
# DELETE       to delete something
#
# json:{
#     its imformation,  to delete data we need to pass what  kind of data we want to delete as similar for others
# }
#
#
# Response
#
# Status: 200 sucesss
# 404 not found
# 400 bad req
# 403 unauthorized

from flask import (request, jsonify)

from config import app, db
from models import Contact


@app.route("/contacts", methods=["GET"])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify({"contacts": json_contacts})


@app.route("/", methods=["GET"])
def get_hello():
    return jsonify({"contacts": "Hello Me pagal hi hu"})


@app.route("/create_contact", methods=["POST"])
def create_contact():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return jsonify({"message": "you must include a first name,last name and email"}), 400,

    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    return jsonify({"message": "User created!"}), 201


@app.route("/update_contact/<int:user_id>", methods=["PATCH"])
def update_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "user not found"}), 404

    contact.first_name = request.json.get("firstName", contact.first_name)
    contact.last_name = request.json.get("lastName", contact.last_name)
    contact.email = request.json.get("email", contact.email)

    db.session.commit()

    return jsonify({"message": "User updated."}), 200


@app.route("/delete_contact/<int:user_id>", methods=["DELETE"])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({"message": "user not found"}), 404

    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "User deleted!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
