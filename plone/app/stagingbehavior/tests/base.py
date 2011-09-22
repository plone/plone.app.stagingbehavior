from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting


class Fixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.stagingbehavior
        import plone.app.versioningbehavior
        self.loadZCML(package=plone.app.stagingbehavior)
        self.loadZCML(package=plone.app.versioningbehavior)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.stagingbehavior:testfixture')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="plone.app.stagingbehavior:Integration",
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="plone.app.stagingbehavior:Functional",
    )