# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer


class AppTagsServiceGet(Service):
    def reply(self):
        result = {
            "app-tags": {"@id": "{}/@app-tags".format(self.context.absolute_url())}
        }
        tags = api.portal.get_registry_record("udala.jakinarazpenak.tags")
        result["items"] = tags
        return result
