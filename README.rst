**********************
django CMS URL Manager
**********************

============
Installation
============

Requirements
============

django CMS URL Manager requires that you have a django CMS 4.0 or higher.

For those who wish to use this app on Django <3.2 or Python <3.8 use the 4.0.x branch.


To install
==========

Run::

    pip install djangocms-url-manager

Add ``djangocms_url_manager`` to your project's ``INSTALLED_APPS``.

Run::

    python manage.py migrate djangocms_url_manager

to perform the application's database migrations.


=====
Usage
=====

Migration 0008 requires the use of a user in order to create versions for existing urls (if djangocms_versioning is installed and enabled), a user can be chosen with the setting DJANGOCMS_URL_MANAGER_VERSIONING_MIGRATION_USER_ID, the default is 1.


    DJANGOCMS_URL_MANAGER_VERSIONING_MIGRATION_USER_ID = 2 # Will use user with id: 2
