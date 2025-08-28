from plone import api
from udala.jakinarazpenak import _
from udala.jakinarazpenak.interfaces import INotification
from udala.jakinarazpenak.interfaces import INotificationsUtility
from z3c.form import button
from z3c.form import field
from z3c.form import form
from z3c.form import validator
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.interfaces import HIDDEN_MODE
from zope.component import getUtility
from zope.interface import Invalid


class MissingTags(Invalid):
    __doc__ = _("Tags are required")


class TooManyTags(Invalid):
    __doc__ = _("You can select max. 5 tags")


class TagValidator(validator.SimpleFieldValidator):
    def validate(self, value):
        super(TagValidator, self).validate(value)
        if not value:
            raise MissingTags(_("Tags are required"))

        if len(value) > 5:
            raise TooManyTags(_("You can select max. 5 tags"))


validator.WidgetValidatorDiscriminators(TagValidator, field=INotification["tags"])


class NotificationsEditView(form.Form):
    fields = field.Fields(INotification).omit("created", "sent", "sent_date")
    ignoreContext = False

    label = _("Edit a notification")

    # @property
    # def description(self):
    #     portal = api.portal.get()
    #     url = "{0}/@@notifications-management-view".format(portal.absolute_url())
    #     return _(
    #         '<a href="${url}">Manage all notifications here</a>', mapping={"url": url}
    #     )

    def _get_id(self):
        id = self.request.get("id", None)

        if id is None:
            # Check if we are submitting the form and get the id from there
            id = self.request.get("form.widgets.id", None)

        return id

    def updateWidgets(self):
        super(NotificationsEditView, self).updateWidgets()
        self.request.set("disable_border", True)
        self.fields["tags"].widgetFactory = CheckBoxFieldWidget
        self.widgets["id"].mode = HIDDEN_MODE

    def update(self):
        super(NotificationsEditView, self).update()
        self.actions["save"].klass += " btn-primary"
        self.actions["send"].klass += " btn-primary"

    def getContent(self):
        id = self._get_id()
        notification_utility = getUtility(INotificationsUtility)
        notification = notification_utility.get_notification_by_id(id)
        return notification.to_dict()

    @button.buttonAndHandler(_("Save notification"), name="save")
    def handleApplyEdit(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _("There were errors processing the form")
            return

        notification_utility = getUtility(INotificationsUtility)
        notification_utility.edit_notification(data.get("id"), data)

        api.portal.show_message(
            _("Notification was edited correctly"), type="info", request=self.request
        )

        url = f"{self.context.absolute_url()}/@@notifications-edit-view?id={data.get('id')}"
        return self.request.response.redirect(url)

    @button.buttonAndHandler(_("Send notification"), name="send")
    def handleApplySend(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = _("There were errors processing the form")
            return

        notification_utility = getUtility(INotificationsUtility)
        data["sent"] = True
        notification_utility.edit_notification(data.get("id"), data)
        result = notification_utility.send_notification(data.get("id"))
        if result:
            api.portal.show_message(
                _("Notification was sent correctly"), type="info", request=self.request
            )
        else:
            api.portal.show_message(
                _("There was an error sending the notification. Please try again."),
                type="error",
                request=self.request,
            )
        url = f"{self.context.absolute_url()}/@@notifications-edit-view?id={data.get('id')}"
        return self.request.response.redirect(url)

    @button.buttonAndHandler(_("Back"), name="back")
    def handleApplyBack(self, action):
        portal = api.portal.get()
        url = f"{portal.absolute_url()}/@@notifications-management-view"
        return self.request.response.redirect(url)
