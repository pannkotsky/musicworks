import factory

from works.models import Contributor, ContributorWork, Source, Work


class ContributorFactory(factory.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')

    class Meta:
        model = Contributor


class SourceFactory(factory.DjangoModelFactory):
    identifier = factory.Faker('domain_word')

    class Meta:
        model = Source
        django_get_or_create = ('identifier',)


class WorkFactory(factory.DjangoModelFactory):
    iswc = factory.Sequence(lambda n: f'T{n:010d}')
    source = factory.SubFactory(SourceFactory)
    id_from_source = factory.Sequence(lambda n: n)
    title = factory.Faker('sentence')

    class Meta:
        model = Work

    @factory.post_generation
    def contributors(self, create, extracted, **kwargs):
        if extracted:
            for item in extracted:
                ContributorWorkFactory(contributor=item, work=self)


class ContributorWorkFactory(factory.DjangoModelFactory):
    contributor = factory.SubFactory(ContributorFactory)
    work = factory.SubFactory(WorkFactory)

    class Meta:
        model = ContributorWork
