#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource

from config import app, db, api
from models import User


class ClearSession(Resource):
    def delete(self):
        session["page_views"] = None
        session["user_id"] = None

        return {}, 204


class Signup(Resource):
    def post(self):
        json = request.get_json()
        user = User(username=json["username"], password_hash=json["password"])
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id

        return user.to_dict(), 201


class CheckSession(Resource):
    def get(self):
        user_id = session["user_id"]
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return make_response(user.to_dict(), 200)
        return make_response({}, 204)


class Login(Resource):
    def post(self):
        json = request.get_json()
        user = User.query.filter(User.username == json["username"]).first()

        if user.authenticate(json["password"]):
            session["user_id"] = user.id
            return user.to_dict(), 200
        return {"message": "unauthorized"}, 401


class Logout(Resource):
    def delete(self):
        print(session["user_id"])
        session["user_id"] = None
        return {}, 204


api.add_resource(ClearSession, "/clear", endpoint="clear")
api.add_resource(Signup, "/signup", endpoint="signup")
api.add_resource(CheckSession, "/check_session")
api.add_resource(Login, "/login")
api.add_resource(Logout, "/logout")

if __name__ == "__main__":
    app.run(port=5555, debug=True)
