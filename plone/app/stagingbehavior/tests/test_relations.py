from unittest2 import TestCase
from Acquisition import aq_base
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent

from plone.dexterity.utils import createContentInContainer
from plone.locking.interfaces import ILockable

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles


from plone.app.iterate.interfaces import IBaseline
from plone.app.iterate.interfaces import ICheckinCheckoutPolicy

from plone.app.stagingbehavior.tests.base import INTEGRATION_TESTING
from plone.app.stagingbehavior.interfaces import IWCAnnotator
from plone.app.stagingbehavior.utils import get_checkout_relation


class TestObjectsRelations(TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        super(TestObjectsRelations, self).setUp()

        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        # create a folder where everything of this test suite should happen
        self.assertNotIn('test-folder', self.portal.objectIds())
        self.folder = self.portal.get(
            self.portal.invokeFactory('Folder', 'test-folder'))

    def tearDown(self):
        self.portal.manage_delObjects([self.folder.id])
        logout()
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        super(TestObjectsRelations, self).tearDown()

    def do_checkout(self, obj):
        policy = ICheckinCheckoutPolicy(obj)
        working_copy = policy.checkout(self.folder)
        return working_copy

    def do_cancel(self, working_copy):
        policy = ICheckinCheckoutPolicy(working_copy)
        policy.cancelCheckout()

    def do_checkin(self, working_copy):
        policy = ICheckinCheckoutPolicy(working_copy)
        return policy.checkin('')

    def test_after_checkout(self):
        baseline = createContentInContainer(self.folder, 'stageable_type')

        working_copy = self.do_checkout(baseline)
        relation = IWCAnnotator(baseline).get_relation()

        self.assertEqual(relation.to_object, working_copy)
        self.assertEqual(relation.from_object, baseline)

        self.assertEqual(get_checkout_relation(baseline), relation)

    def test_after_cancel_checkout(self):
        """When user cancel checkout relation to baseline is None"""
        baseline = createContentInContainer(self.folder, 'stageable_type')

        working_copy = self.do_checkout(baseline)
        self.do_cancel(working_copy)

        relation = IWCAnnotator(baseline).get_relation()
        self.assertIsNone(relation)
        self.assertIsNone(get_checkout_relation(baseline))

    def test_after_checkin(self):
        baseline = createContentInContainer(self.folder, 'stageable_type')

        working_copy = self.do_checkout(baseline)
        new_baseline = self.do_checkin(working_copy)

        relation = IWCAnnotator(new_baseline).get_relation()
        self.assertIsNone(relation)
        self.assertIsNone(get_checkout_relation(new_baseline))

    def test_edit_baseline(self):
        """Some time somebody can edit a IBaseline object
        and updateRelations subscriber in z3c.relationfield package,
        will delete all reference before to update them.
        """
        baseline = createContentInContainer(self.folder, 'stageable_type')
        working_copy = self.do_checkout(baseline)
        baseline.title = u'new title'

        # XXX: aq_base is necessary to prevent error:
        # "TypeError: Can't pickle objects in acquisition wrappers."
        # in CMFEdition
        notify(ObjectModifiedEvent(aq_base(baseline)))

        relation = get_checkout_relation(baseline)
        annotation = IWCAnnotator(baseline).get_relation()
        self.assertIsNotNone(relation)
        self.assertEqual(relation, annotation)

    # def test_delete_working_copy(self):
    #     baseline = createContentInContainer(self.folder, 'stageable_type')
    #     working_copy = self.do_checkout(baseline)
    #     wc_id = working_copy.id
    #     self.folder.manage_delObjects([wc_id])

    #     self.assertNotIn(wc_id, self.folder.objectIds())
    #     self.assertFalse(IBaseline.providedBy(baseline))
    #     self.assertFalse(ILockable(baseline).locked())
