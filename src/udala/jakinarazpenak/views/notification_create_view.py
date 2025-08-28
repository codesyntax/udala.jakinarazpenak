from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from udala.jakinarazpenak.interfaces import INotificationsUtility
from zope.component import getUtility
from zope.interface import alsoProvides


class NotificationCreateView(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)

        data = self.get_notification_data()

        notification_utility = getUtility(INotificationsUtility)
        created_id = notification_utility.add_notification(data)
        nav_root = api.portal.get_navigation_root(self.context)
        url = f"{nav_root.absolute_url()}/@@notifications-edit-view?id={created_id}"
        return self.request.response.redirect(url)

    def get_notification_data(self):
        return {
            "title": self.context.Title(),
            "summary": self.context.Description(),
            "language": self.context.Language(),
            "url": self.context.absolute_url(),
            "tags": [],
        }


class EmptyNotificationCreateView(NotificationCreateView):
    def get_notification_data(self):
        language = api.portal.get_current_language()
        return {"title": "", "summary": "", "language": language, "url": "", "tags": []}
