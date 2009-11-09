
from five import grok

from plone.app.iterate.browser import info
from plone.app.iterate.interfaces import IBaseline, IWorkingCopy
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.memoize.instance import memoize

from plone.stagingbehavior.interfaces import IStagingSupport
from plone.stagingbehavior.utils import get_baseline, get_working_copy, get_checkout_relation


class BaselineInfoViewlet( info.BaselineInfoViewlet, grok.Viewlet ):
    grok.name( 'plone.app.iterate.baseline_info' )
    grok.viewletmanager( IAboveContent )
    grok.require( 'zope2.View' )
    grok.context( IStagingSupport )
    grok.implements( IViewView )


    def render(self):
        if IBaseline.providedBy(self.context):
            return info.BaselineInfoViewlet.render(self)
        return ''

    def _getReference( self ):
        return get_checkout_relation( self.context )


    @memoize
    def working_copy( self ):
        return get_working_copy( self.context )


    @property
    @memoize
    def properties( self ):
        relation = get_checkout_relation( self.context )
        if relation:
            return relation.staging_properties
        else:
            return None




class CheckoutInfoViewlet( info.CheckoutInfoViewlet, grok.Viewlet ):
    grok.name( 'plone.app.iterate.checkout_info' )
    grok.viewletmanager( IAboveContent )
    grok.require( 'zope2.View' )
    grok.context( IStagingSupport )
    grok.implements( IViewView )


    def render(self):
        if IWorkingCopy.providedBy(self.context):
            return info.CheckoutInfoViewlet.render(self)
        return ''


    def _getReference( self ):
        return get_checkout_relation( self.context )


    @memoize
    def baseline( self ):
        return get_baseline( self.context )


    @property
    @memoize
    def properties( self ):
        relation = get_checkout_relation( self.context )
        if relation:
            return relation.staging_properties
        else:
            return None

