
from five import grok
from zc.relation.interfaces import ICatalog
from Acquisition import aq_inner
from zope.app.intid.interfaces import IIntIds
from zope import component

from plone.app.iterate.browser import info
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.memoize.instance import memoize
from plone.stagingbehavior.interfaces import IStagingSupport
from plone.stagingbehavior import STAGING_RELATION_NAME


class BaselineInfoViewlet( info.BaselineInfoViewlet, grok.Viewlet ):
    grok.name( 'plone.app.iterate.baseline_info' )
    grok.viewletmanager( IAboveContent )
    grok.require( 'zope2.View' )
    grok.context( IStagingSupport )
    grok.implements( IViewView )

    @memoize
    def get_relation(self):
        context = aq_inner( self.context ) 
        # get id
        intids = component.getUtility( IIntIds )
        id = intids.getId( context )
        # ask catalog
        catalog = component.getUtility( ICatalog )
        relations = list(catalog.findRelations({ 'from_id' : id }))
        relations = filter( lambda r:r.from_attribute==STAGING_RELATION_NAME,
                            relations )
        if len( relations ) > 0:
            return relations[0]
        else:
            return None

    @memoize
    def working_copy( self ):
        relation = self.get_relation()
        intids = component.getUtility( IIntIds )
        if relation:
            id = relation.to_id
            return intids.getObject(id)
        else:
            return None

    @property
    @memoize
    def properties( self ):
        return self.get_relation().staging_properties


class CheckoutInfoViewlet( info.CheckoutInfoViewlet, grok.Viewlet ):
    grok.name( 'plone.app.iterate.checkout_info' )
    grok.viewletmanager( IAboveContent )
    grok.require( 'zope2.View' )
    grok.context( IStagingSupport )
    grok.implements( IViewView )

    @memoize
    def get_relation(self):
        context = aq_inner( self.context ) 
        # get id
        intids = component.getUtility( IIntIds )
        id = intids.getId( context )
        # ask catalog
        catalog = component.getUtility( ICatalog )
        relations = list(catalog.findRelations({ 'to_id' : id }))
        relations = filter( lambda r:r.from_attribute==STAGING_RELATION_NAME,
                            relations )
        if len( relations ) > 0:
            return relations[0]
        else:
            return None

    @memoize
    def baseline( self ):
        relation = self.get_relation()
        intids = component.getUtility( IIntIds )
        if relation:
            id = relation.from_id
            return intids.getObject(id)
        else:
            return None

    @property
    @memoize
    def properties( self ):
        return self.get_relation().staging_properties

