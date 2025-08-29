from plone import api
from Products.Five.browser import BrowserView
from udala.jakinarazpenak import _
from udala.jakinarazpenak.interfaces import INotificationsUtility
from zope.component import getUtility


class DeleteAllNotificationsView(BrowserView):
    def __call__(self):
        utility = getUtility(INotificationsUtility)
        utility.delete_all_notifications()
        url = f"{self.context.absolute_url}/notifications-management-view"
        api.portal.show_message(
            _("Notifications were deleted correctly"), type="info", request=self.request
        )
        return self.request.response.redirect(url)
