=========
Changelog
=========

1.2.0 (2024-05-16)
==========
* Python 3.10 support added
* Django 4.2 support added
* Django < 3.2 support removed


1.1.0 (2022-02-22)
==================
* Python 3.8, 3.9 support added
* Django 3.0, 3.1 and 3.2 support added
* Python 3.5 and 3.6 support removed
* Django 1.11 support removed

1.0.0.dev2 (2021-02-16)
=======================
* fix: Pinned versioning to a dj1.11 compatible version for the test suite.
* fix: Attempt at fixing installation errors

1.0.0.dev1 (2021-12-06)
=======================
* Added djangocms-versioning support
    - Added grouper model
    - Added versioning config in cms_config
    - Added versioning copy method
    - Added versioning testing factory models
    - Data migration added for Url Grouper model
    - Reworked forms and views for versioning support
    - Removed internal_name field from LinkPlugin model. Added migration for the link plugin

* Github Actions integration

0.0.11 (2021-05-17)
===================
* Fixed missing migration and initial migration dependencies on the cms
* Removed Python 3.5 EOL and added Python 3.7 and 3.8 in the tox and CircleCI configs
