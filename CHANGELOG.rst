=========
Changelog
=========

Unreleased
==========


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
