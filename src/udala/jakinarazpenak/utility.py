# -*- coding: utf-8 -*-
from BTrees.OOBTree import OOBTree
from persistent.list import PersistentList
from plone import api
from Products.CMFPlone.utils import safe_text
from udala.jakinarazpenak import FIREBASE_URL
from udala.jakinarazpenak.notification import Notification
from udala.jakinarazpenak.notification import send_topic_push
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory

import datetime
import pytz
import uuid


ANNOTATION_KEY = "udala.jakinarazpenak.annotattion"


def current_date():
    my_date = datetime.datetime.now(pytz.timezone("Europe/Madrid"))
    return my_date.isoformat()


class NotificationsUtility(object):
    def __init__(self):
        self.annotations = []

    def initialize(self):
        if not self.annotations:
            portal = api.portal.get()
            annotations = IAnnotations(portal)
            if ANNOTATION_KEY not in annotations:
                annotations[ANNOTATION_KEY] = PersistentList()

            self.annotations = annotations[ANNOTATION_KEY]

    def _initialize(self):
        portal = api.portal.get()
        annotations = IAnnotations(portal)
        if ANNOTATION_KEY not in annotations:
            annotations[ANNOTATION_KEY] = PersistentList()

        return annotations[ANNOTATION_KEY]

    def _record_to_notification(self, record):
        n = Notification()
        for k, v in record.items():
            setattr(n, k, v)

        return n

    def delete_all_notifications(self):
        self._save_all_annotations(PersistentList())

    def _save_all_annotations(self, annotations):
        portal = api.portal.get()
        IAnnotations(portal)[ANNOTATION_KEY] = annotations

    def _add_to_annotation(self, record):
        annotations = self._initialize()
        annotations.append(record)
        self._save_all_annotations(annotations)

    def _save_to_annotation(self, notification_id, record):
        annotations = self._initialize()
        new_values = PersistentList()
        for annotation in annotations:
            if annotation["id"] == notification_id:
                new_values.append(record)
            else:
                new_values.append(annotation)

        self._save_all_annotations(new_values)

    def get_notifications(self):
        annotations = self._initialize()
        items = [self._record_to_notification(annotation) for annotation in annotations]

        return sorted(items, key=lambda x: x.created, reverse=True)

    def get_notifications_by_tags(self, tags):
        annotations = self._initialize()
        items = [item for item in annotations if set(tags).intersection(item["tags"])]
        return [self._record_to_notification(item) for item in items]

    def get_notifications_by_tag_and_language(self, tags, lang):
        annotations = self._initialize()
        items = [
            item
            for item in annotations
            if set(tags).intersection(item["tags"]) and lang == item["language"]
        ]
        return [self._record_to_notification(item) for item in items]

    def get_notification_by_id(self, notification_id=None):
        annotations = self._initialize()
        items = [item for item in annotations if item["id"] == notification_id]
        if items:
            return self._record_to_notification(items[0])

        return None

    def get_notification_record_by_id(self, notification_id=None):
        annotations = self._initialize()
        items = [item for item in annotations if item["id"] == notification_id]
        if items:
            return items[0]

        return None

    def add_notification(self, data={}):
        record = OOBTree()
        notification_id = data.get("id", None)
        if notification_id is None:
            notification_id = uuid.uuid4().hex

        # Guarantee unique publication id
        while self.get_notification_by_id(notification_id) is not None:
            notification_id = uuid.uuid4().hex

        record["id"] = safe_text(notification_id)
        record["title"] = safe_text(data.get("title", ""))
        record["summary"] = safe_text(data.get("summary", ""))
        record["url"] = safe_text(data.get("url", ""))
        record["tags"] = data.get("tags", [])
        record["language"] = safe_text(data.get("language", "eu"))
        record["created"] = safe_text(current_date())
        record["sent"] = False
        record["sent_date"] = None

        self._add_to_annotation(record)

        return notification_id

    def edit_notification(self, notification_id, data={}):
        notification = self.get_notification_by_id(notification_id)
        if notification is not None:
            # Extract this to get_notification_record
            record = self.get_notification_record_by_id(notification_id)
            if record is not None:
                if data.get("title", None) is not None:
                    record["title"] = safe_text(data.get("title"))
                if data.get("summary", None) is not None:
                    record["summary"] = safe_text(data.get("summary"))
                if data.get("url", None) is not None:
                    record["url"] = safe_text(data.get("url"))
                if data.get("language", None) is not None:
                    record["language"] = safe_text(data.get("language"))
                if data.get("tags", None) is not None:
                    record["tags"] = tuple(data.get("tags", []))
                if data.get("sent", None) is not None:
                    record["sent"] = True
                    record["sent_date"] = safe_text(current_date())

            self._save_to_annotation(notification_id, record)

            return True

        return False

    def mark_as_sent(self, notification_id):
        return self.edit_notification(notification_id, {"sent": True})

    def send_notification(self, notification_id):
        notification = self.get_notification_by_id(notification_id)
        if notification is not None:

            my_date = safe_text(current_date())

            topics = [
                "{0}_{1}".format(tag, notification.language)
                for tag in notification.tags
            ]

            topic_names = [
                self.get_tag_name(tag)
                for tag in notification.tags
                if self.get_tag_name(tag) is not None
            ]

            data = {
                "title": notification.title,
                "summary": notification.summary,
                # "tags": notification.tags,
                "topics": str(topics),
                "topic_names": str(topic_names),
                "url": notification.url,
                "date": safe_text(my_date),
            }
            if len(topics) == 1:
                try:
                    topic = topics[0]
                    send_topic_push(
                        topic, notification.title, notification.summary, data
                    )
                    return True
                except Exception as e:
                    from logging import getLogger

                    log = getLogger(__name__)
                    log.info("Error sending the notification")
                    log.info(str(e))
                    return False
            else:
                try:
                    for topic in topics:
                        send_topic_push(
                            topic, notification.title, notification.summary, data
                        )
                    return True
                except Exception as e:
                    from logging import getLogger

                    log = getLogger(__name__)
                    log.info("Error sending the notification")
                    log.info(str(e))
                    return False
        return False

    def get_tag_name(self, tag):
        vocabulary_factory = getUtility(
            IVocabularyFactory, name="udala.jakinarazpenak.AppTagsVocabulary"
        )
        vocabulary = vocabulary_factory()
        try:
            return vocabulary.getTerm(tag).title
        except LookupError:
            return None
