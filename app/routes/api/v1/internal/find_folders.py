"""Find Folders"""

from . import internal
from ....main.utils import private_endpoint
from .....static.python.mongodb import read
from .....static.python.classes import Folder, Course


@internal.route("/find-folders/<id>", methods=["POST"])
@private_endpoint
def connect_schoology(id):
    courseid = id
    course = read.find_courses(courseid)
    folders = course.folders
    string = "0"
    for i in folders:
        string += " • "
        string += str(i._id)
    return string