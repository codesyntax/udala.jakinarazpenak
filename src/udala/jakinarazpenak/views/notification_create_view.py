# -*- coding: utf-8 -*-
from udala.jakinarazpenak import _
from udala.jakinarazpenak.interfaces import INotification
from udala.jakinarazpenak.interfaces import INotificationsUtility
from udala.jakinarazpenak.notification import Notification
from plone import api
from plone.autoform.directives import widget
from Products.Five.browser import BrowserView
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form.interfaces import HIDDEN_MODE
from zope import schema
from zope.component import getUtility
from plone.protect.interfaces import IDisableCSRFProtection
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
