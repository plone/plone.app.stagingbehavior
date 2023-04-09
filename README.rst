This repository is archived and read only.

If you want to unarchive it, then post to the [Admin & Infrastructure (AI) Team category on the Plone Community Forum](https://community.plone.org/c/aiteam/55).

Introduction
============

The ``IStagingSupport`` behavior is used for enabling the plone.app.iterate
functionality for Dexterity content. It allows you to perform the checkout
and checkin operations to work on a copy of your original content.

Compatibility
-------------

Plone 5's version of plone.app.iterate implements dexterity support making this package absolete. This package is only useful in Plone 4.

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

