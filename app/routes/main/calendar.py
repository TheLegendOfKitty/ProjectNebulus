from flask import render_template, session

from app.static.python.mongodb.read import getText
from . import main_blueprint
from .utils import logged_in


@main_blueprint.route("/calendar", methods=["GET"])
@logged_in
def calendar():
    return render_template(
        "learning/tools/calendar.html",
        user=session["username"],
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        email=session["email"],
        page="Nebulus - Calendar",
        translate=getText,
    )
