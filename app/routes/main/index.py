from flask import render_template, session, redirect, request

from . import main_blueprint


@main_blueprint.route("/", methods=["GET"])
def index():
    # return "hi"
    return render_template(
        "main/index.html",
        page="Nebulus - Learning, All In One",
        user=session.get("username"),
        email=session.get("email"),
        avatar=session.get("avatar"),
    )


@main_blueprint.route("/google34d8c04c4b82b69a.html")
def googleVerification():
    # GOOGLE VERIFICATION FILE
    return render_template("google34d8c04c4b82b69a.html")


@main_blueprint.route("/arc-sw.js")
def arcstuff():
    return redirect("https://arc.io/arc-sw.js")


@main_blueprint.route("/privacy-policy")
def pp():
    return redirect("https://privacypolicy.nebuluslms.repl.co/")


@main_blueprint.route("/terms-of-service")
def tos():
    return redirect(
        "https://docs.google.com/document/d/1XjNHjBRS2xJWKObo_zuQ2oPVSKQ8EK8Y_o8e77VPZf4/edit"
    )


@main_blueprint.app_errorhandler(404)
@main_blueprint.app_errorhandler(400)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html"), 404


@main_blueprint.app_errorhandler(500)
def internal_error(e):
    # note that we set the 404 status explicitly
    return render_template("errors/500.html"), 500
