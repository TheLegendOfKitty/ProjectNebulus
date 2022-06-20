from flask import Blueprint


static_blueprint = Blueprint(
    "static_blueprint",
    __name__,
    url_prefix="/static",
    template_folder="../templates",
    static_folder="../static",
)

from .static_1layer import *
from .static_2layer import *
