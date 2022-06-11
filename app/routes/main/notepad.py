from flask import render_template, session

from . import main_blueprint
from ...static.python.mongodb import read


@main_blueprint.route("/notepad", methods=["GET"])
def notepad():
    fonts = [
        "Arial",
        "Times New Roman",
        "Comic Sans MS",
        "Pacifico",
        "Roboto",
        "Lobster",
        "Lato",
        "Montserrat",
        "Raleway",
        "Roboto Condensed",
        "Open Sans",
        "Roboto Slab",
        "Merriweather",
        "Ubuntu",
        "PT Sans",
        "PT Serif",
        "Ubuntu Condensed",
        "Droid Sans",
        "Droid Serif",
        "Roboto Mono",
        "Roboto Mono Condensed",
        "Roboto Mono Slashed",
        "Roboto Mono Slashed Condensed",
        "Roboto Mono Slashed Slashed",
        "Roboto Mono Slashed Slashed Condensed",
    ]
    return render_template(
        "notepad.html",
        page="Nebulus - Notepad",
        user=session.get("username"),
        avatar="/static/images/nebulusCats" + session.get("avatar", "/v3.gif"),
        read=read,
        fonts=fonts,
    )
