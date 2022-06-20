from flask import render_template, session

from app.routes.main.utils import logged_in
from . import main_blueprint
from ...static.python.mongodb import read


@main_blueprint.route("/planner", methods=["GET"])
@logged_in
def planner():
    return render_template(
        "tools/planner.html",
        page="Nebulus - Planner",
        user=session.get("username"),
        email=session.get("email"),
        avatar=session.get("avatar", "/static/images/nebulusCats/v3.gif"),
        read=read,
    )
