from djangocms_url_manager.compat import DJANGO_4_1


if DJANGO_4_1:  # TODO: remove when dropping support for Django < 4.2
    from django.test.testcases import TransactionTestCase

    TransactionTestCase.assertQuerySetEqual = TransactionTestCase.assertQuerysetEqual
