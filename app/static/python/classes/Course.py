from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    EmbeddedDocumentField,
    ListField,
    ReferenceField,
    StringField,
)

from .Avatar import Avatar
from .Snowflake import Snowflake

templates = (
    "Sports",
    "Math",
    "Science",
    "Language",
    "History",
    "Art",
    "Music",
    "Other",
)


class Course(Snowflake):
    """
    A subclass of the Snowflake object, representing a course.
    Has many bidirectional references to other objects.
        - Folders - (A list of folders in the course.) -> course.folders -> folder.course
        - Assignments - (The assignments that are in the course) -> course.assignments -> assignment.course
        - Grades - (A list of complete grades for the course) -> course.grades -> grades.course
        - Events - (The events that are associated with this course) -> course.events -> event.course
        - Users (The users that are enrolled in the course) -> course.authorizedUsers -> user.courses
    """

    meta = {"collection": "Courses"}
    name = StringField(required=True)
    teacher = StringField(required=True)
    teacherAccount = ReferenceField("User")
    created_at = DateTimeField(default=lambda: datetime.now())
    template = StringField(default=None)
    # sub_template = StringField(default=None)
    authorizedUsers = ListField(ReferenceField("User"))
    assignments = ListField(ReferenceField("Assignment"))
    folders = ListField(ReferenceField("Folder"))
    description = StringField(default="", null=True)
    documents = ListField(ReferenceField("DocumentFile"))
    grades = ReferenceField("Grades")
    events = ListField(ReferenceField("Event"))
    avatar = EmbeddedDocumentField(Avatar, required=False)
    announcements = ListField(ReferenceField("Announcement"))
    archived = BooleanField(default=False)
    integrations = ListField(ReferenceField("Integration"))
    textbooks = ListField(ReferenceField("Textbook"))

    def clean(self):
        if not self.avatar:
            self.avatar = Avatar(
                avatar_url="https://app.schoology.com/sites/all/themes/schoology_theme/images/course-default.svg"
            )
