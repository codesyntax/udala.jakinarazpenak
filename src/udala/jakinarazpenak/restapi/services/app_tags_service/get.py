from plone import api
from plone.restapi.services import Service


class AppTagsServiceGet(Service):
    def reply(self):
        result = {"app-tags": {"@id": f"{self.context.absolute_url()}/@app-tags"}}
        tags = api.portal.get_registry_record("udala.jakinarazpenak.tags")
        result["items"] = tags
        return result
