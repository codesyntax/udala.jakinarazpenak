# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield.registry import DictRow
from udala.jakinarazpenak import _
from plone import api
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from plone.autoform.directives import widget
from zope import schema
from zope.interface import Interface


class ITableRowSchema(Interface):
    number = schema.Int(title=_("Tag number"))
    eu = schema.TextLine(title=_("Tag name in basque"))
    es = schema.TextLine(title=_("Tag name in spanish"))


class IFirebaseControlPanel(Interface):

    # firebase_adminsdk_json = JSONField(
    #     title=_(u"Firebase admin SDK JSON"),
    #     description=_(u"Enter the Firebase API key used to send notifications"),
    #     required=False,
    # )
    firebase_adminsdk_json = schema.TextLine(
        title=_("Firebase admin SDK JSON"),
        description=_("Enter the Firebase admin SDK JSON used to send notifications"),
        required=True,
    )

    widget(tags=DataGridFieldFactory)
    tags = schema.List(
        title=_("Tags"),
        value_type=DictRow(title=_("Tag"), schema=ITableRowSchema),
        default=[],
        required=False,
    )


class FirebaseControlPanelForm(RegistryEditForm):
    schema = IFirebaseControlPanel
    schema_prefix = "udala.jakinarazpenak"
    label = _("Firebase Settings")


FirebaseControlPanelView = layout.wrap_form(
    FirebaseControlPanelForm, ControlPanelFormWrapper
)
