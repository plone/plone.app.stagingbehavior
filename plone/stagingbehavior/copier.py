
from Acquisition import aq_inner, aq_parent, aq_base
from five import grok
from zope import component
from zope.app.intid.interfaces import IIntIds
from zope.schema import getFieldsInOrder
from z3c.relationfield import event
from zc.relation.interfaces import ICatalog
from ZODB.PersistentMapping import PersistentMapping

from plone.app.iterate import copier
from plone.app.iterate import interfaces
from plone.relations.relationships import Z2Relationship as Relationship
from plone.dexterity.utils import iterSchemata
from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

from plone.stagingbehavior.interfaces import IStagingSupport
from plone.stagingbehavior.relation import StagingRelationValue
from plone.stagingbehavior import STAGING_RELATION_NAME

class ContentCopier( copier.ContentCopier, grok.Adapter ):
    grok.implements( interfaces.IObjectCopier )
    grok.context( IStagingSupport )

    def copyTo( self, container ):
        context = aq_inner( self.context )
        wc = self._copyBaseline( container )
        # get id of objects
        intids = component.getUtility( IIntIds )
        wc_id = intids.getId( wc )
        context_id = intids.getId( self.context )
        # create a relation
        relation = StagingRelationValue( wc_id )
        event._setRelation( context, STAGING_RELATION_NAME, relation )
        #
        self._handleReferences( self.context, wc, 'checkout', relation )
        return wc, relation

    def merge( self ):
        baseline = self._getBaseline()

        # delete the working copy reference to the baseline
        wc_ref = self._deleteWorkingCopyRelation()

        # reassemble references on the new baseline
        self._handleReferences( baseline, self.context, "checkin", wc_ref )

        # move the working copy to the baseline container, deleting the baseline
        new_baseline = self._replaceBaseline( baseline )

        # patch the working copy with baseline info not preserved during checkout
        self._reassembleWorkingCopy( new_baseline, baseline )

        return new_baseline

    def _replaceBaseline( self, baseline ):
        wc_id = self.context.getId()
        wc_container = aq_parent( self.context )

        # copy all field values from the working copy to the baseline
        for schema in iterSchemata( baseline ):
            for name, field in getFieldsInOrder( schema ):
                try:
                    value = field.get( schema( self.context ) )
                except:
                    value = None
                field.set( baseline, value )
        baseline.processForm()
        # delete the working copy

        wc_container._delObject( wc_id )
        return baseline

    def _reassembleWorkingCopy( self, new_baseline, baseline ):
        # reattach the source's workflow history, try avoid a dangling ref
        try:
            new_baseline.workflow_history = PersistentMapping( baseline.workflow_history.items() )
        except AttributeError:
            # No workflow apparently.  Oh well.
            pass

        # reset wf state security directly
        workflow_tool = getToolByName(self.context, 'portal_workflow')
        wfs = workflow_tool.getWorkflowsFor( self.context )
        for wf in wfs:
            if not isinstance( wf, DCWorkflowDefinition ):
                continue
            wf.updateRoleMappingsFor( new_baseline )

        # reattach the source's uid, this will update wc refs to point back to the new baseline
        # XXX
        #new_baseline._setUID( baseline.UID() )

        # reattach the source's history id, to get the previous version ancestry
        # XXX
        histid_handler = getToolByName( self.context, 'portal_historyidhandler')
        #huid = histid_handler.getUid( baseline )
        #histid_handler.setUid( new_baseline, huid, check_uniqueness=False )

        return new_baseline

    def _handleReferences( self, baseline, wc, mode, wc_ref ):
        pass

    def _deleteWorkingCopyRelation( self ):
        # delete the wc reference keeping a reference to it for its annotations
        relation = self._get_relation_to_baseline()
        relation.broken(relation.to_path)
        return relation

    def _get_relation_to_baseline( self ):
        context = aq_inner( self.context )
        # get id
        intids = component.getUtility( IIntIds )
        id = intids.getId( context )
        # ask catalog
        catalog = component.getUtility( ICatalog )
        relations = list(catalog.findRelations({ 'to_id' : id }))
        relations = filter( lambda r:r.from_attribute==STAGING_RELATION_NAME,
                            relations )
        # do we have a baseline in our relations?
        if relations and not len(relations) == 1:
            raise iterate.interfaces.CheckinException( "Baseline count mismatch" )

        if not relations or not relations[0]:
            raise iterate.interfaces.CheckinException( "Baseline has disappeared" )
        return relations[0]

    def _getBaseline( self ):
        intids = component.getUtility( IIntIds )
        relation = self._get_relation_to_baseline()
        if relation:
            baseline = intids.getObject( relation.from_id )

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

