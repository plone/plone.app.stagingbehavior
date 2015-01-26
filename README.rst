Introduction
============

The ``IStagingSupport`` behavior is used for enabling the plone.app.iterate
functionality for Dexterity content. It allows you to perform the checkout
and checkin operations to work on a copy of your original content.


Usage
-----

Just use the behavior ``plone.app.stagingbehavior.interfaces.IStagingSupport``
in your Dexterity content-type.

In your *profiles/default/types/YOURTYPE.xml* add the behavior::

    <?xml version="1.0"?>
    <object name="example.conference.presenter" meta_type="Dexterity FTI"
       i18n:domain="example.conference" xmlns:i18n="http://xml.zope.org/namespaces/i18n">

     <!-- enabled behaviors -->
     <property name="behaviors">
         <element value="plone.app.stagingbehavior.interfaces.IStagingSupport" />
     </property>

    </object>


The IStagingSupport behavior just adds the referred staging support to your
content-type, but it does not enable it.

You have to set the "versioning" option in the Plone types control panel
(/@@types-controlpanel) to either "Manual" or "Automatic" for activating
versioning.


More Information
----------------

For more information about how the staging works see the documentation of
plone.app.iterate and Products.CMFEdtitions:

* http://pypi.python.org/pypi/plone.app.iterate
* http://pypi.python.org/pypi/Products.CMFEditions

