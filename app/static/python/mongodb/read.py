from __future__ import annotations

import json

import schoolopy
from flask import session
from mongoengine import Q

from app.static.python.classes import *
from app.static.python.utils.security import valid_password

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

dictionary = None


def getText(query):
    global dictionary
    if not dictionary:
        with open("app/static/python/dictionary.json") as dictFile:
            dictionary = json.loads(dictFile.read())

    try:
        return dictionary[query][session.get("global", "us")]
    except KeyError:
        return query


def getAssignment(assignment_id: str) -> Assignment:
    assignment = Assignment.objects(id=assignment_id).first()
    return assignment


def getNebulusDocument(document_id: str) -> NebulusDocument:
    document = NebulusDocument.objects(id=document_id).first()
    return document


def getEvent(event_id: str) -> Event:
    event = Event.objects(pk=event_id).first()
    return event


def getGrades(grades_id: str) -> Grades:
    grades = Grades.objects(pk=grades_id).first()
    return grades


def getDocumentFile(document_file_id: str) -> DocumentFile:
    document_file = DocumentFile.objects(pk=document_file_id).first()
    return document_file


def getFolder(folder_id: str) -> Folder:
    folder = Folder.objects(pk=folder_id).first()
    return folder


def get_user_courses(user_id: str) -> list[Course]:
    user = find_user(pk=user_id)
    return Course.objects(authorizedUsers=user)


def get_user_docs(user_id: str) -> list[NebulusDocument]:
    user = find_user(pk=user_id)
    return NebulusDocument.objects(authorizedUsers=user)


def search_user(query: str, ignore_id: str = None) -> list[User]:
    if ignore_id:
        return User.objects(username__istartswith=query, id__ne=ignore_id).only(
            "id", "username", "email", "avatar", "_cls"
        )[:10]
    else:
        return User.objects(username__istartswith=query).only(
            "id", "username", "email", "avatar", "_cls"
        )[:10]
    # return User.objects.filter(username__contains=query)._query


def search_within_course(query: str, course_id: str):
    assignments = Assignment.objects(course_id=course_id, title__contains=query)
    events = Event.objects(course_id=course_id, title__contains=query)
    document_file = DocumentFile.objects(course_id=course_id, title__contains=query)


def find_courses(_id: str):
    course = Course.objects(pk=_id)
    if not course:
        raise KeyError("Course not found")
    return course[0]


def find_user(**kwargs) -> User | None:
    data = {k: v for k, v in kwargs.items() if v is not None}
    user = User.objects(**data).first()
    if not user:
        raise KeyError("User not found")

    return user


def find_folder(**kwargs) -> Folder | None:
    folder = Folder.objects(**kwargs).first()
    if not folder:
        print(folder)
        raise KeyError("Folder not found")
    return folder


def find_document(**kwargs) -> Document | None:
    document = DocumentFile.objects(**kwargs).first()
    if not document:
        print(document)
        raise KeyError("User not found")
    return document


def getSchoology(**kwargs) -> list[Schoology] | None:
    try:
        return find_user(**kwargs).schoology
    except KeyError:
        return


def getClassroom(
        userID: str = None, username: str = None, email: str = None
) -> GoogleClassroom:
    return find_user(id=userID, username=username, email=email).gclassroom


def getSpotify(userID: str = None, username: str = None, email: str = None) -> Spotify:
    return find_user(id=userID, username=username, email=email).spotify


def getSpotifyCache(
        userID: str = None, username: str = None, email: str = None
) -> Spotify | None:
    try:
        return find_user(
            id=userID, username=username, email=email
        ).spotify.Spotify_cache
    except:
        return None


def checkSchoology(_id: int):
    user = find_user(id=_id)
    return str(user and user.schoology).lower()


def check_type(o):
    try:
        a = find_folder(**o)
        if a is None:
            return "document"
        else:
            return "folder"
    except:
        return "document"


def check_signin(email, password):
    try:
        user = find_user(email=email)
    except KeyError:
        return False

    return valid_password(user.password, password)


def get_announcement(announcement_id: str) -> Announcement:
    announcement = Announcement.objects(pk=announcement_id).first()
    return announcement


def get_folders(parent_id: int = None, course_id: int = None) -> list[Folder]:
    if not parent_id and not course_id:
        raise ValueError("Must provide either parent_id or course_id")

    if course_id:
        return find_courses(course_id).folders
    else:
        return find_folder(id=parent_id).subfolders


def sortByDate(obj):
    return obj.date.date() if obj._cls == "Event" else obj.due.date()


def sortByDateTime(obj):
    return obj.date if obj._cls == "Event" else obj.due


def sort_course_events(user_id: str, course_id: int):
    courses = get_user_courses(user_id)
    course = None
    for i in courses:
        if str(i.id) == str(course_id):
            course = i
            break
    courses = [course]

    events = Event.objects(course__in=courses)
    announcements = Announcement.objects(course__in=courses)
    assignments = Assignment.objects(course__in=courses)
    assessments = Assessment.objects(course__in=courses)
    from itertools import chain, groupby

    events_assessments_assignments = list(chain(events, assignments, assessments))
    sorted_events = sorted(
        events_assessments_assignments, key=lambda obj: sortByDateTime(obj)
    )
    dates = dict(
        {
            key: list(result)
            for key, result in groupby(
            sorted_events, key=lambda obj: sortByDateTime(obj)
        )
        }
    )

    sorted_announcements = sorted(announcements, key=lambda obj: obj.date)
    announcements = dict(
        reversed(
            list(
                {
                    key: list(result)
                    for key, result in groupby(
                    sorted_announcements, key=lambda obj: obj.date.date()
                )
                }.items()
            )
        )
    )

    return [announcements, dates]


def sort_user_events(user_id: str, maxDays=5, maxEvents=16):
    courses = get_user_courses(user_id)
    events = Event.objects(course__in=courses)
    announcements = Announcement.objects(course__in=courses)
    assignments = Assignment.objects(course__in=courses)
    assessments = Assessment.objects(course__in=courses)
    from itertools import chain, groupby

    events_assessments_assignments = list(chain(events, assignments, assessments))
    sorted_events = reversed(
        sorted(
            events_assessments_assignments[:maxEvents],
            key=lambda obj: sortByDateTime(obj),
        )
    )

    dates = dict(
        {
            key: list(result)
            for key, result in groupby(
            sorted_events, key=lambda obj: sortByDateTime(obj)
        )
        }
    )

    sorted_announcements = sorted(announcements, key=lambda obj: obj.date)
    announcements = dict(
        reversed(
            list(
                {
                    key: list(result)
                    for key, result in groupby(
                    sorted_announcements, key=lambda obj: obj.date.date()
                )
                }.items()
            )[-maxDays:]
        )
    )

    return [announcements, dates]

    # events_assessments_assignments = events | assignments | assessments


def unsorted_user_events(user_id: str) -> list[list]:
    courses = get_user_courses(user_id)
    events = Event.objects(course__in=courses)
    announcements = Announcement.objects(course__in=courses)
    assignments = Assignment.objects(course__in=courses)
    assessments = Assessment.objects(course__in=courses)
    from itertools import chain

    events_assessments_assignments = list(chain(events, assignments, assessments))
    announcements = list(reversed(announcements))
    return [
        announcements,
        sorted(events_assessments_assignments, key=lambda obj: sortByDateTime(obj)),
    ]


def getSchoologyAuth(user_id) -> schoolopy.Schoology | None:
    schoology = getSchoology(id=user_id)
    if not schoology:
        return

    schoology = schoology[0]
    request_token = schoology.Schoology_request_token
    request_token_secret = schoology.Schoology_request_secret
    access_token = schoology.Schoology_access_token
    access_token_secret = schoology.Schoology_access_secret
    link = schoology.schoologyDomain
    key = schoology.apikey
    secret = schoology.apisecret
    auth = schoolopy.Auth(
        key,
        secret,
        domain=link,
        three_legged=True,
        request_token=request_token,
        request_token_secret=request_token_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    auth.authorize()
    sc = schoolopy.Schoology(auth)
    sc.limit = 5

    return sc


def check_signup_user(username) -> str:
    if User.objects(username=username):
        return "false"
    return "true"


def check_signup_email(email) -> str:
    if User.objects(email=email):
        return "false"
    return "true"


def check_duplicate_schoology(schoology_email) -> str:
    if User.objects(schoology__schoologyEmail=schoology_email):
        return "true"
    return "false"


def getChat(chat_id: str):
    chat = Chat.objects.get(pk=chat_id)
    if not chat:
        raise KeyError("Invalid Chat ID")

    return chat


def getPlanner(user_id: str):
    planner = find_user(id=user_id).planner
    if not planner:
        return {}

    return {
        "name": planner.name,
        "saveData": planner.saveData,
        "periods": planner.periods,
        "lastEdited": planner.lastEdited,
    }


def getDocument(document_id: str):  # Nebulus Document
    doc = NebulusDocument.objects(pk=document_id)
    if not doc:
        raise KeyError("Invalid Document ID")
    return doc


def search(keyword: str, username: str):
    user = User.objects(username=username).first()
    users = search_user(keyword)
    pipeline1 = [
        {"$match": {"title": {"$regex": f"^{keyword}", "$options": "i"}}},
        {
            "$lookup": {
                "from": Course._get_collection_name(),
                "localField": "course",
                "foreignField": "_id",
                "as": "course",
            }
        },
        {"$match": {"course.authorizedUsers": user.pk}},
        {"$project": {"title": 1, "_id": 1, "_cls": 1}},
    ]
    courses = Course.objects(Q(authorizedUsers=user.id) & Q(name__istartswith=keyword))[
              :10
              ]
    chats = Chat.objects(Q(owner=user.id) & Q(title__istartswith=keyword))[:10]
    NebulusDocuments = NebulusDocument.objects(
        Q(authorizedUsers=user.id) & Q(title__istartswith=keyword)
    )[:10]

    events = list(Event.objects().aggregate(pipeline1))
    assignments = list(Assignment.objects().aggregate(pipeline1))
    announcements = list(Announcement.objects().aggregate(pipeline1))
    documents = list(DocumentFile.objects.aggregate(pipeline1))
    return (
        courses,
        documents,
        chats,
        events,
        assignments,
        announcements,
        NebulusDocuments,
        users,
    )


def search_course(keyword: str, course: str):
    course = Course.objects(id=course).first()
    pipeline1 = [
        {"$match": {"title": {"$regex": f"^{keyword}", "$options": "i"}}},
        {
            "$lookup": {
                "from": Course._get_collection_name(),
                "localField": "course",
                "foreignField": "_id",
                "as": "course",
            }
        },
        {"$match": {"course.id": course}},
        {"$project": {"title": 1, "_id": 1, "_cls": 1}},
    ]

    events = list(Event.objects().aggregate(pipeline1))
    assignments = list(Assignment.objects().aggregate(pipeline1))
    announcements = list(Announcement.objects().aggregate(pipeline1))
    documents = list(DocumentFile.objects.aggregate(pipeline1))
    return (
        documents,
        events,
        assignments,
        announcements,
        # NebulusDocuments,
    )


def getUserChats(user_id, required_fields: list):
    chats = Chat.objects(members__user=user_id).only(*required_fields)
    return chats


def loadChats(user_id: str, current_index, initial_amount, required_fields):
    chats = json.loads(getUserChats(user_id, required_fields).to_json())

    chats = sorted(chats, key=lambda x: x["lastEdited"]["$date"], reverse=True)

    if len(chats) < current_index + initial_amount:
        initial_amount = len(chats) - current_index

    chats = chats[current_index: (current_index + initial_amount)]
    for chat in chats:
        if len(chat["members"]) == 2:
            for x, member in enumerate(chat["members"]):
                chat["members"][x]["user"] = json.loads(
                    User.objects.only(
                        "id", "chatProfile", "username", "avatar.avatar_url"
                    )
                    .get(pk=member["user"])
                    .to_json()
                )
                chat["members"][x]["unread"] = str(chat["members"][x]["unread"])
            chat["owner"] = list(
                filter(lambda x: x["user"]["_id"] == chat["owner"], chat["members"])
            )[0]

    print(chats)
    return chats


def get_friends(user_id):
    user = find_user(pk=user_id)
    try:
        friends = user.chatProfile.friends
    except:
        friends = None
    return friends


def get_blocks(user_id):
    user = find_user(pk=user_id)
    try:
        blocked = user.chatProfile.blocked
    except:
        blocked = None
    return blocked


def get_user_notepad(user):
    user = find_user(pk=user)
    try:
        # print(user.notepad)
        notepad = dict(user.notepad.data)
    except Exception as e:

        print(e)
        notepad = {}
    return notepad
