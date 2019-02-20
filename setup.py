from setuptools import find_packages, setup

import djangocms_url_manager


INSTALL_REQUIREMENTS = ["Django>=1.11,<2.2", "django-cms>=3.5,<4.1", "djangocms-attributes-field>=0.1.1"]


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
    url="http://github.com/divio/djangocms-url-manager",
    license="BSD",
    test_suite="test_settings.run",
)
