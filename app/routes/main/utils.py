from __future__ import annotations

import datetime
from functools import wraps

from flask import redirect, render_template, request, session

try:
    from ...static.python.mongodb import read
except ImportError:
    ...

SCHOOLOGY_COURSE_ICON = "https://app.schoology.com/sites/all/themes/schoology_theme/images/course-default.svg"


def logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("username"):
            try:
                read.find_user(id=session.get("id"))
                return func(*args, **kwargs)
            except KeyError:
                return redirect("/logout")
        else:
            return redirect("/signin?redirect=" + request.path)

    wrapper.__name__ = func.__name__
    return wrapper


def private_endpoint(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.headers.getlist("X-Forwarded-For"):
            user_ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            user_ip = request.remote_addr

        # the first parameter should be the flask server ip address, so change it to what the ip is for your server

        if (
                str(user_ip) == "127.0.0.1" or "2600:1700:5450:7b08:9806:a9a9:a039:e92e"
        ):  # server ip
            return func(*args, **kwargs)
        else:
            return render_template("errors/404.html", error="Unauthorized Access"), 405

    wrapper.__name__ = func.__name__
    return wrapper


def strftime(time: datetime.date, fmt) -> str:
    try:
        return time.strftime(fmt)

    except ValueError:
        if "-" in fmt:
            fmt = fmt.replace("-", "#")
        else:
            fmt = fmt.replace("#", "-")

        return time.strftime(fmt)
