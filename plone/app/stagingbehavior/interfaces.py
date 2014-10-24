from zope.interface import Interface
from zope.interface import Attribute
from z3c.relationfield.interfaces import IRelationValue

from plone.locking.interfaces import ITTWLockable
from plone.app.iterate.interfaces import IIterateAware


class IStagingSupport(IIterateAware, ITTWLockable):
    """ Behavior interface for enabling staging with plone.app.iterate
    """


class IStagingRelationValue(IRelationValue):
    """
    """
    staging_properties = Attribute('Staging information')


class IWCAnnotator(Interface):
    """Working copy relation annotator.
    This adapter stores StagingRelationValue in IBaseline object
    in order to prevent to lose working copy relation when
    IBaseLine is changed"""
