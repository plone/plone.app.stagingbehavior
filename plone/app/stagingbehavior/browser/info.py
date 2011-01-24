from five import grok

from plone.app.iterate.browser import info
from plone.app.iterate.interfaces import IBaseline, IWorkingCopy
from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets.interfaces import IAboveContent
from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.stagingbehavior.utils import get_baseline
from plone.app.stagingbehavior.utils import get_working_copy
from plone.app.stagingbehavior.utils import get_checkout_relation
from plone.app.stagingbehavior.interfaces import IStagingSupport


class BaselineInfoViewlet( info.BaselineInfoViewlet, grok.Viewlet ):
    grok.name( 'plone.app.iterate.baseline_info' )
    grok.viewletmanager( IAboveContent )
    grok.require( 'zope2.View' )
    grok.context( IStagingSupport )
    grok.implements( IViewView )

    template = ViewPageTemplateFile('info_baseline.pt')

    def render(self):
        if IBaseline.providedBy(self.context) and self.working_copy() is not None:
            return self.template()
        return ''

    def _getReference( self ):
        return get_checkout_relation( self.context )

    @memoize
    def working_copy( self ):
        return get_working_copy( self.context )

    def creator(self):
        local_roles = self.working_copy().get_local_roles()
        if len(local_roles)==1:
            user_id = local_roles[0][0]
            return self.context.portal_membership.getMemberById(user_id)
        else:
            return info.BaseInfoViewlet.creator(self)

    @property
    def linked_working_copy(self):
        member = self.context.portal_membership.getAuthenticatedMember()
        return member.getId() == self.creator().getId()

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
