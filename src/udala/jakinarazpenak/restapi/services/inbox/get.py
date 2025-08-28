from plone.restapi.batching import HypermediaBatch
from udala.jakinarazpenak.interfaces import INotificationsUtility
from udala.jakinarazpenak.restapi.services.notifications.get import NotificationsGet
from zope.component import getUtility


class InboxGet(NotificationsGet):
    def reply(self):
        results = {"@id": f"{self.context.absolute_url()}/@inbox"}

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

        items = []
        for notification in notifications:
            item = notification.to_dict()
            item = self.transform_item(item)
            items.append(item)

        items.sort(key=lambda x: x["created"], reverse=True)

        batch = HypermediaBatch(self.request, items)

        results["items_total"] = batch.items_total
        if batch.links:
            results["batching"] = batch.links

        results["items"] = [item for item in batch]

        return results
