from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

import factory
from djangocms_versioning.models import Version
from factory.fuzzy import FuzzyText

from djangocms_url_manager.models import Url, UrlGrouper


class UserFactory(factory.django.DjangoModelFactory):
    username = FuzzyText(length=12)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda u: "%s.%s@example.com" % (u.first_name.lower(), u.last_name.lower())
    )

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the default ``_create`` with our custom call."""
        manager = cls._get_manager(model_class)
        # The default would use ``manager.create(*args, **kwargs)``
        return manager.create_user(*args, **kwargs)


class AbstractVersionFactory(factory.django.DjangoModelFactory):
    object_id = factory.SelfAttribute("content.id")
    content_type = factory.LazyAttribute(
        lambda o: ContentType.objects.get_for_model(o.content)
    )
    created_by = factory.SubFactory(UserFactory)

    class Meta:
        exclude = ["content"]
        abstract = True


class UrlGrouperFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = UrlGrouper


class AbstractUrlFactory(factory.django.DjangoModelFactory):
    url_grouper = factory.SubFactory(UrlGrouperFactory)
    url = factory.SubFactory(UserFactory)
    internal_name = FuzzyText(length=10)
    date_modified = factory.Faker('date_object')

    class Meta:
        abstract = True


class UrlFactory(AbstractUrlFactory):
    class Meta:
        model = Url


class UrlVersionFactory(AbstractVersionFactory):
    content = factory.SubFactory(UrlFactory)

    class Meta:
        model = Version


class UrlWithVersionFactory(AbstractUrlFactory):
    @factory.post_generation
    def version(self, create, extracted, **kwargs):
        # NOTE: Use this method as below to define version attributes:
        # PageContentWithVersionFactory(version__label='label1')
        if not create:
            # Simple build, do nothing.
            return
        UrlVersionFactory(content=self, **kwargs)

    class Meta:
        model = Url
