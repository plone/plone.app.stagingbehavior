from Acquisition import aq_inner
from five import grok
from zc.relation.interfaces import ICatalog
from zope import component
from zope.app.intid.interfaces import IIntIds
from zope.event import notify

from plone.app import iterate
from plone.app.stagingbehavior.utils import get_baseline
from plone.app.stagingbehavior.utils import get_relations
from plone.app.stagingbehavior.interfaces import IStagingSupport


class CheckinCheckoutPolicyAdapter(iterate.policy.CheckinCheckoutPolicyAdapter,
                                   grok.Adapter):
    """
    Dexterity Checkin Checkout Policy
    """
    grok.implements( iterate.interfaces.ICheckinCheckoutPolicy )
    grok.context( IStagingSupport )

    def _get_relation_to_baseline( self ):
        # do we have a baseline in our relations?
        relations = get_relations( self.context )

        if relations and not len( relations ) == 1:
            raise iterate.interfaces.CheckinException( "Baseline count mismatch" )

        if not relations or not relations[0]:
            raise iterate.interfaces.CheckinException( "Baseline has disappeared" )

        return relations[0]

    def _getBaseline( self ):
        baseline = get_baseline( self.context )
        if not baseline:
            raise iterate.interfaces.CheckinException( "Baseline has disappeared" )
        return baseline

    def checkin( self, checkin_message ):
        # get the baseline for this working copy, raise if not found
        baseline = self._getBaseline()
        # get a hold of the relation object
        relation = self._get_relation_to_baseline()
        # publish the event for subscribers, early because contexts are about to be manipulated
        notify( iterate.event.CheckinEvent( self.context,
                                            baseline,
                                            relation,
                                            checkin_message
        ) )
        # merge the object back to the baseline with a copier
        copier = component.queryAdapter( self.context,
                                         iterate.interfaces.IObjectCopier )
        new_baseline = copier.merge()
        # don't need to unlock the lock disappears with old baseline deletion
        notify( iterate.event.AfterCheckinEvent( new_baseline, checkin_message ) )
        return new_baseline
