from setuptools import find_packages, setup

import djangocms_url_manager


INSTALL_REQUIREMENTS = [
    "Django>=1.11,<3.0",
    "django-cms",
    "djangocms-attributes-field",
]


setup(
    name="djangocms-url-manager",
    packages=find_packages(),
    include_package_data=True,
    version=djangocms_url_manager.__version__,
    description=djangocms_url_manager.__doc__,
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
    ],
    install_requires=INSTALL_REQUIREMENTS,
    author="Divio AG",
    author_email="info@divio.ch",
    maintainer='Django CMS Association and contributors',
    maintainer_email='info@django-cms.org',
    url="https://github.com/django-cms/djangocms-url-manager",
    license="BSD",
    test_suite="test_settings.run",
)
