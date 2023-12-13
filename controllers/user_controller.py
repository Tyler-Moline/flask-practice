from flask import jsonify, request
import json
from uuid import uuid4


def database_read():
    try:
        with open("database.json", "r") as openfile:

            return json.load(openfile)

    except:

        return []


def database_write(records):
    with open("database.json", "w") as outfile:
        json.dump(records, outfile)


def user_add():
    post_data = request.form if request.form else request.json

    user = {
        "user_id": str(uuid4()),
        "first_name": post_data["first_name"],
        "last_name": post_data["last_name"],
        "email": post_data["email"],
        "phone": post_data["phone"],
        "active": True
    }

    user_records = database_read()
    user_records.append(user)

    database_write(user_records)

    return jsonify(f'user {user["name"]} has been added '), 201


def user_get_all():
    user_records = database_read()

    if len(user_records) == 0:
        return jsonify("no user records were found"), 404

    return jsonify(user_records), 200


def user_get_by_id(user_id):
    user_records = database_read()

    if len(user_records) == 0:
        return jsonify("no user records were found"), 404

    for user in user_records:
        if user["user_id"] == user_id:

            return jsonify(user), 200

    return jsonify(f"user with id: {user_id} not found"), 404


def user_activity(user_id):
    user_records = database_read()

    if len(user_records) == 0:
        return jsonify("no user records were found"), 404

    for user in user_records:
        if user["user_id"] == user_id:

            return jsonify(user), 200

    return jsonify(f"user with id: {user_id} not found"), 404


def user_update_by_id(user_id):

    user_records = database_read()

    post_data = request.form if request.form else request.json

    if len(user_records) == 0:

        return jsonify(f"no user records found", 404)

    for user in user_records:
        if user["user_id"] == user_id:

            for key in list(user.keys()):
                try:
                    user[key] = post_data[key]

                except:
                    pass

            database_write(user_records)

            return jsonify(f"user with user_id: {user} was updated]")
    return jsonify(f"user with user_id: {user_id} NOT FOUND")
