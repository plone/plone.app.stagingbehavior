from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig

class Fixture(PloneSandboxLayer):
    default_bases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.stagingbehavior
        xmlconfig.include(configurationContext, 'configure.zcml', plone.app.stagingbehavior)
        configurationContext.execute_actions()

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.stagingbehavior:testfixture')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name="plone.app.stagingbehavior:Integration",
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name="plone.app.stagingbehavior:Functional",
    )