
from persistent.dict import PersistentDict
from zope.interface import implements
from zope.annotation.interfaces import IAttributeAnnotatable

from z3c.relationfield import relation

from plone.stagingbehavior.interfaces import IStagingRelationValue

class StagingRelationValue(relation.RelationValue):
    implements(IStagingRelationValue, IAttributeAnnotatable)

    def __init__(self, to_id):
        super(StagingRelationValue, self).__init__(to_id)
        self.staging_properties = PersistentDict()

