
#from AccessControl import getSecurityManager
#from Products.Five.browser import BrowserView
#from Products.Archetypes.interfaces import IReferenceable
#import Products.CMFCore.permissions

#from plone.app.iterate.relation import WorkingCopyRelation
#from plone.app.iterate import permissions

from five import grok
from Acquisition import aq_inner

from z3c.relationfield.interfaces import IHasRelations

from plone.memoize.view import memoize

from plone.app.iterate import interfaces
from plone.app.iterate.browser import control

from plone.stagingbehavior.interfaces import IStagingSupport

class Control(control.Control):
    """Information about whether iterate can operate.
    
    This is a public view, referenced in action condition expressions.
    """
    
    def get_original(self, context):
        # XXX
        raise NotImplemented
        if IReferenceable.providedBy(context):
            refs = context.getRefs(WorkingCopyRelation.relationship)
            if refs:
                return refs[0]

    def checkin_allowed(self):
        """Check if a checkin is allowed
        """
        context = aq_inner(self.context)

        if not IHasRelations.providedBy(context):
            return False
        # XXX
        return True
        raise NotImplemented
        checkPermission = getSecurityManager().checkPermission
        
        if not interfaces.IIterateAware.providedBy(context):
            return False
    
        archiver = interfaces.IObjectArchiver(context)
        if not archiver.isVersionable():
            return False

        original = self.get_original(context)
        if original is None:
            return False

        if not checkPermission(
            Products.CMFCore.permissions.ModifyPortalContent, original):
            return False
        
        return True
        
    def checkout_allowed(self):
        """Check if a checkout is allowed.
        """
        context = aq_inner(self.context)

        if not IHasRelations.providedBy(context):
            return False
        
        archiver = interfaces.IObjectArchiver(context)
        if not archiver.isVersionable():
            return False

        # XXX
        return True
        # check if there is an existing checkout
        if len(context.getBRefs(WorkingCopyRelation.relationship)) > 0:
            return False
        
        # check if its is a checkout
        if len(context.getRefs(WorkingCopyRelation.relationship)) > 0:
            return False
        
        return True
        
    @memoize
    def cancel_allowed(self):
        """Check to see if the user can cancel the checkout on the
        given working copy
        """
        context = aq_inner(self.context)

        if not IHasRelations.providedBy(context):
            return False
        return True
        # XXX
        raise NotImplemented
        return self.get_original(aq_inner(self.context)) is not None
