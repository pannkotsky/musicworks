from django.test import TestCase

from works.models import Contributor
from works.serializers import ContributorSerializer, ContributorsField, SourceField
from .factories import ContributorFactory, SourceFactory


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
        self.assertEqual(c, value[0])
        self.assertEqual('Martin', value[1].first_name)
        self.assertEqual('Gore', value[1].last_name)

    def test_representation(self):
        ContributorFactory(first_name='Dave', last_name='Gahan')
        ContributorFactory(first_name='Martin', last_name='Gore')
        value = ContributorsField().to_representation(Contributor.objects)
        self.assertEqual('Dave Gahan|Martin Gore', value)
