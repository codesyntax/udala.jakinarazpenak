# -*- coding: utf-8 -*-
from DateTime import DateTime
from plone.restapi.services import Service
from udala.jakinarazpenak.interfaces import INotificationsUtility
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class NotificationsGet(Service):
    def reply(self):
        """tags parameter should contain "tagid_lang" items:
        1_es
        2_es,3_es
        ...
        """

        result = []
        notification_utility = getUtility(INotificationsUtility)
        tags = self.request.get("tags", None)
        if tags is not None:
            tags = tags.split(",")
            tags = [tag.split("_") for tag in tags if len(tag.split("_")) == 2]
            if tags:
                language = tags[0][1]
                tags = [int(tag[0]) for tag in tags if tag[0].isdigit()]

                notifications = (
                    notification_utility.get_notifications_by_tag_and_language(
                        tags, language
                    )
                )
            else:
                notifications = []

        else:
            notifications = notification_utility.get_notifications()

        for notification in notifications:
            item = notification.to_dict()
            item = self.transform_item(item)
            result.append(item)

        return {"data": result}

    def transform_item(self, item):
        new_tags = []
        for tag in item["tags"]:
            name = self.get_tag_name(tag)
            if name is not None:
                new_tags.append(self.get_tag_name(tag))

        item["tag_names"] = new_tags
        # item["created"] = self.toLocalizedTime(item["created"])
        # item["sent_date"] = self.toLocalizedTime(item["sent_date"])

        item["created"] = item["created"]
        item["sent_date"] = item["sent_date"]

        return item

    def get_tag_name(self, tag):
        vocabulary_factory = getUtility(
            IVocabularyFactory, name="udala.jakinarazpenak.AppTagsVocabulary"
        )
        vocabulary = vocabulary_factory(self.context)
        try:
            return vocabulary.getTerm(tag).title
        except LookupError:
            return None

    def toLocalizedTime(self, value):
        if value:
            dt = DateTime(value)
            plone_view = getMultiAdapter((self.context, self.request), name="plone")
            return plone_view.toLocalizedTime(dt, True)

        return ""
