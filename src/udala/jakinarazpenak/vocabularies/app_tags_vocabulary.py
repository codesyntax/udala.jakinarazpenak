# from plone import api
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class VocabItem:
    def __init__(self, token, value):
        self.token = token
        self.value = value


@implementer(IVocabularyFactory)
class AppTagsVocabulary:
    """ """

    def __call__(self, context=None):
        # Just an example list of content for our vocabulary,
        # this can be any static or dynamic data, a catalog result for example.
        items = []

        if not IDexterityContent.providedBy(context):
            req = getRequest()
            context = req.PARENTS[0]

        language = api.portal.get_current_language()
        tags = api.portal.get_registry_record("udala.jakinarazpenak.tags")
        for tag in tags:
            items.append(
                VocabItem(tag["number"], (language == "eu" and tag["eu"]) or tag["es"])
            )

        # create a list of SimpleTerm items:
        terms = []
        for item in items:
            terms.append(
                SimpleTerm(value=item.token, token=str(item.token), title=item.value)
            )
        # Create a SimpleVocabulary from the terms list and return it:
        return SimpleVocabulary(terms)


AppTagsVocabularyFactory = AppTagsVocabulary()
