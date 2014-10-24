import logging
from Acquisition import aq_base
from zope.event import notify
from z3c.relationfield.event import _setRelation
from plone.app.iterate.interfaces import IWorkingCopy
from plone.app.iterate.event import WorkingCopyDeletedEvent
from plone.app.stagingbehavior.utils import get_checkout_relation
from plone.app.stagingbehavior.interfaces import IWCAnnotator
from plone.app.stagingbehavior import STAGING_RELATION_NAME

logger = logging.getLogger('plone.app.stagingbehavior')


def _store_relation(obj, relation):
    """Annotate to baseline the relation
    with its working copy"""
    storage = IWCAnnotator(obj, None)
    if storage:
        storage.set_relation(relation)

        logger.info(
            'Annotate WC relation: {}'.format(
                '/'.join(obj.getPhysicalPath())
            )
        )


def _delete_relation(obj):
    """Delete working copy relation annotation"""
    storage = IWCAnnotator(obj, None)
    if storage:
        storage.delete()

        logger.info(
            'Delete WC annotation: {}'.format(
                '/'.join(obj.getPhysicalPath())
            )
        )


def handleCancelCheckout(event):
    """Delete relation from baseline object"""
    _delete_relation(event.baseline)


def updateRelations(obj, event):
    storage = IWCAnnotator(obj)
    if storage:
        _setRelation(obj, STAGING_RELATION_NAME, storage.get_relation())
