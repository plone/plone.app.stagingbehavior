from Acquisition import aq_base
from persistent import Persistent
from persistent.dict import PersistentDict
from zc.relation.interfaces import ICatalog
from zope.app.intid.interfaces import IIntIds
from zope.interface import implements
from zope.component import getUtility
from zope.component import adapts
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.annotation import factory

from z3c.relationfield import relation

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName

from plone.dexterity.interfaces import IDexterityContent

from plone.app.stagingbehavior.interfaces import IWCAnnotator
from plone.app.stagingbehavior.interfaces import IStagingRelationValue


class StagingRelationValue(relation.RelationValue):
    implements(IStagingRelationValue, IAttributeAnnotatable)

    @classmethod
    def get_relations_of( cls, obj, from_attribute=None ):
        """ a list of relations to or from the passed object
        """
        catalog = getUtility( ICatalog )
        intids = getUtility( IIntIds )
        obj_id = intids.getId( obj )
        items = list( catalog.findRelations({
                    'from_id' : obj_id,
                    }) )
        items += list( catalog.findRelations({
                    'to_id' : obj_id,
                    }))
        if from_attribute:
            condition = lambda r:r.from_attribute==from_attribute and \
                not r.is_broken()
            items = filter( condition, items )
        return items

    def __init__(self, to_id):
        super(StagingRelationValue, self).__init__(to_id)
        self.staging_properties = PersistentDict()
        # remember the creator
        portal = getUtility(ISiteRoot)
        mstool = getToolByName(portal, 'portal_membership')
        self.creator = mstool.getAuthenticatedMember().getId()


class Storage(Persistent):
    implements(IWCAnnotator)
    adapts(IDexterityContent)

    def __init__(self):
        super(Storage, self).__init__()
        self._data = None

    def set_relation(self, value):
        # dewrap __parent__ attribute,
        # CMFEdition cannot pickle wrapped objects
        value.__parent__ = aq_base(value.__parent__)
        self._data = value

    def get_relation(self):
        return self._data

    def delete(self):
        self._data = None


WCAnnotator = factory(Storage)
