from mongoengine import *
from .User import User


class ChatProfile(EmbeddedDocument):
    """
    A class representing a user's Chat Profile
    """

    friends = ListField(ReferenceField("User"))
    acceptingFriendRequests = BooleanField(default=True)
    incomingFriendRequests = ListField(ReferenceField("User"))
    outgoingFriendRequests = ListField(ReferenceField("User"))
    blocked = ListField(ReferenceField("User"))
    mutedDMS = ListField(ReferenceField("Chat"))
    # TODO: mutedThreads
    mutedCommunities = ListField(ReferenceField("Community"))
    DM_Open = ListField(ReferenceField("User"))
    text_status = StringField()
    status_emoji = StringField()  # twemoji
    status = StringField()  # Online, Idle, Do Not Disturb, Offline
    custom_emojis = ListField(StringField())
