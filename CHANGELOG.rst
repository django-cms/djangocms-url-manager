=========
Changelog
=========

Unreleased
==========
* Added djangocms-versioning support
    - Added grouper model
    - Added versioning config in cms_config
    - Added versioning copy method
    - Added versioning testing factory models
    - Data migration added for Url Grouper model
    - Reworked forms and views for versioning support
* Github Actions integration
* Removed internal_name field from LinkPlugin model. Added migration for the link plugin

0.0.11
==========
* Fixed missing migration and initial migration dependencies on the cms
* Removed Python 3.5 EOL and added Python 3.7 and 3.8 in the tox and CircleCI configs
