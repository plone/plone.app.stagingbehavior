from Acquisition import aq_inner
from AccessControl import getSecurityManager

from plone.app.iterate import interfaces
from plone.app.iterate.browser import control
from plone.memoize.instance import memoize
from Products.CMFCore.permissions import ModifyPortalContent

from plone.app.stagingbehavior.utils import get_baseline
from plone.app.stagingbehavior.utils import get_working_copy
from plone.app.stagingbehavior.utils import get_checkout_relation


class Control(control.Control):
    """Information about whether iterate can operate.

    This is a public view, referenced in action condition expressions.
    """

    def checkin_allowed(self):
        """ Check if a checkin is allowed.
            Conditions:
            - provides IIterateAware
            - is not baseline
            - is the working copy
            - is versionable
            - user should have ModifyPortalContent permission
        """
        context = aq_inner( self.context )

        if not interfaces.IIterateAware.providedBy( context ):
            return False

        if context == get_baseline( context ):
            return False

        if context != get_working_copy( context ):
            return False

        archiver = interfaces.IObjectArchiver(context)
        if not archiver.isVersionable():
            return False

        checkPermission = getSecurityManager().checkPermission
        if not checkPermission(ModifyPortalContent, context):
            return False

        return True

    def checkout_allowed(self):
        """ Check if a checkout is allowed.
            Conditions:
            - provides IIterateAware
            - is versionable
            - there is no checkout
        """
        context = aq_inner( self.context )

        if not interfaces.IIterateAware.providedBy( context ):
            return False

        archiver = interfaces.IObjectArchiver(context)
        if not archiver.isVersionable():
            return False

        if get_checkout_relation( context ):
            return False

        return True

    @memoize
    def cancel_allowed(self):
        """ Check to see if the user can cancel the checkout on the
            given working copy.
            Conditions:
            - this is a working copy
            - the baseline exists
        """
        context = aq_inner( self.context )

        if context != get_working_copy( context ):
            return False

        if not get_baseline( context ):
            return False

        return True
