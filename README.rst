**********************
django CMS URL Manager
**********************

============
Installation
============

Requirements
============

django CMS URL Manager requires that you have a django CMS 3.5 (or higher) project already running and set up.


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

Migration 0009 requires the use of a user in order to create versions for existing urls (if djangocms_versioning is installed and enabled), a user can be chosen with the setting DJANGOCMS_URL_MANAGER_VERSIONING_MIGRATION_USER_ID, the default is 1.


    DJANGOCMS_URL_MANAGER_VERSIONING_MIGRATION_USER_ID = 2 # Will use user with id: 2
