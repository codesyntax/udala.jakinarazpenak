"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from zope import schema
from zope.interface import Interface

from udala.jakinarazpenak import _

class IBrowserLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class INotification(Interface):
    id = schema.TextLine(
        title=_("Id"), description=_(""), default="", required=False, readonly=False
    )

    title = schema.TextLine(
        title=_("Title"),
        description=_("Enter the title of the notification"),
        default="",
        required=True,
        readonly=False,
    )

    summary = schema.Text(
        title=_("Summary"),
        description=_("Enter the summary text of the notifications"),
        default="",
        required=True,
        readonly=False,
    )

    url = schema.TextLine(
        title=_("URL"),
        description=_("Enter a URL that will be shown with the notification text"),
        required=False,
        readonly=False,
    )

    tags = schema.Set(
        title=_("Tags"),
        description=_("Select the tags of this notification"),
        value_type=schema.Choice(
            vocabulary="udala.jakinarazpenak.AppTagsVocabulary"
        ),
        required=True,
        # defaultFactory=get_default_name,
        readonly=False,
    )

    # Make sure to import: plone.app.vocabularies as vocabs
    language = schema.Choice(
        title=_("Language"),
        description=_("Select the language of this notification"),
        vocabulary="plone.app.vocabularies.SupportedContentLanguages",
        default="",
        # defaultFactory=get_default_language,
        required=False,
        readonly=False,
    )

    created = schema.Datetime(
        title=_("Notification creation date"),
        description=_(""),
        # defaultFactory=get_default_created,
        required=False,
        readonly=False,
    )

    sent = schema.Bool(
        title=_("Has this notification been sent?"),
        description=_(""),
        required=False,
        default=False,
        readonly=False,
    )

    sent_date = schema.Datetime(
        title=_("Notification sent date"),
        description=_(""),
        # defaultFactory=get_default_sent_date,
        required=False,
        readonly=False,
    )

    def to_dict():
        """return a dict with all the attributes"""


class INotificationsUtility(Interface):
    def add_notification(notification_data={}):
        """add a new notification with the data on the parameter. Returns the notification_id"""
