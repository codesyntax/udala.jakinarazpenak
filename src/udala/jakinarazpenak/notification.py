from .interfaces import INotification
from firebase_admin import credentials
from firebase_admin import messaging
from logging import getLogger
from plone import api
from Products.CMFPlone.utils import safe_text
from zope.interface import implementer

import firebase_admin
import json


@implementer(INotification)
class Notification:
    id = ""
    title = ""
    summary = ""
    url = ""
    tags = []
    language = ""
    created = ""
    sent = ""
    sent_date = ""

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "url": self.url,
            "tags": self.tags,
            "language": self.language,
            "created": self.created,
            "sent": self.sent,
            "sent_date": self.sent_date,
        }


def initialize_firebase_app():
    firebase_adminsdk_json = api.portal.get_registry_record(
        "udala.jakinarazpenak.firebase_adminsdk_json"
    )
    if firebase_adminsdk_json:
        firebase_config_file_contents = json.loads(firebase_adminsdk_json)
        cred = credentials.Certificate(firebase_config_file_contents)
        firebase_admin.initialize_app(cred)


def send_topic_push(topic, title, body, data):
    log = getLogger(__name__)

    if not firebase_admin._apps:
        log.info("Initializing firebase app")
        initialize_firebase_app()
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data,
            topic=topic,
        )
        messaging.send(message)
        log.info("Notification sent to topic: %s", safe_text(topic))
    except Exception as e:
        log.info("Error when sending the notification. Exception follows")
        log.exception(e)
