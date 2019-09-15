from django.test import TestCase

from works.models import Contributor
from works.serializers import ContributorSerializer, ContributorsField, SourceField, WorkSerializer
from .factories import ContributorFactory, SourceFactory, WorkFactory


class ContributorSerializerTestCase(TestCase):
    def test_returns_existing_contributor_by_full_name(self):
        c = ContributorFactory(first_name='Dave', last_name='Gahan')
        serializer = ContributorSerializer(data={'full_name': 'Dave Gahan'})
        self.assertTrue(serializer.is_valid())
        c1 = serializer.save()
        self.assertEqual(c, c1)

    def test_creates_new_contributor_by_full_name(self):
        serializer = ContributorSerializer(data={'full_name': 'Martin L. Gore'})
        self.assertTrue(serializer.is_valid())
        c1 = serializer.save()
        self.assertEqual('Martin', c1.first_name)
        self.assertEqual('L.', c1.middle_name)
        self.assertEqual('Gore', c1.last_name)


class SourceFieldTestCase(TestCase):
    def test_internal_value_existing_object(self):
        s = SourceFactory(identifier='warner')
        s1 = SourceField().to_internal_value('warner')
        self.assertEqual(s, s1)

    def test_internal_value_new_object(self):
        s1 = SourceField().to_internal_value('sony')
        self.assertEqual('sony', s1.identifier)

    def test_representation(self):
        s = SourceFactory(identifier='warner')
        self.assertEqual('warner', SourceField().to_representation(s))


class ContributorsFieldTestCase(TestCase):
    def test_internal_value(self):
        c = ContributorFactory(first_name='Dave', last_name='Gahan')
        value = ContributorsField().to_internal_value('Dave Gahan|Martin Gore')
        self.assertEqual(2, len(value))
        self.assertEqual(c.pk, value[0])
        c1 = Contributor.objects.get(pk=value[1])
        self.assertEqual('Martin', c1.first_name)
        self.assertEqual('Gore', c1.last_name)

    def test_representation(self):
        ContributorFactory(first_name='Dave', last_name='Gahan')
        ContributorFactory(first_name='Martin', last_name='Gore')
        value = ContributorsField().to_representation(Contributor.objects)
        self.assertEqual('Dave Gahan|Martin Gore', value)


class WorkSerializerTestCase(TestCase):
    def test_update_matched_instance(self):
        work = WorkFactory(iswc='T0000000009')
        serializer = WorkSerializer(data={
            'iswc': 'T0000000009',
            'source': 'warner',
            'id': 1,
            'title': 'Hello',
            'contributors': 'Adele',
        })
        self.assertTrue(serializer.is_valid())
        self.assertEqual(work, serializer.save())

    def test_create_new_instance(self):
        serializer = WorkSerializer(data={
            'iswc': 'T0000000009',
            'source': 'warner',
            'id': 1,
            'title': 'Hello',
            'contributors': 'Adele',
        })
        self.assertTrue(serializer.is_valid())
        work = serializer.save()
        self.assertEqual(work.iswc, 'T0000000009')
        self.assertEqual(work.source.identifier, 'warner')
        self.assertEqual(work.id_from_source, 1)
        self.assertEqual(work.title, 'Hello')
        self.assertEqual(work.contributors.first().last_name, 'Adele')
