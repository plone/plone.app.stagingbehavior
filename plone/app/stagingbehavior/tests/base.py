from plone.app.testing import PloneSandboxLayer
from plone.app.testing.bbb import PTC_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting

from plone.testing import z2

class Fixture(PloneSandboxLayer):
    defaultBases = (PTC_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.stagingbehavior
        import plone.app.versioningbehavior
        import Products.CMFPlacefulWorkflow
        self.loadZCML(package=plone.app.stagingbehavior)
        self.loadZCML(package=plone.app.versioningbehavior)
        self.loadZCML(package=Products.CMFPlacefulWorkflow)
        z2.installProduct(app, 'Products.CMFPlacefulWorkflow')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.stagingbehavior:testfixture')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(PTC_FIXTURE,),
    name="plone.app.stagingbehavior:Integration",
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(PTC_FIXTURE,),
    name="plone.app.stagingbehavior:Functional",
    )