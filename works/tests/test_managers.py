from django.test import TestCase

from works.managers import ContributorManager
from works.models import Contributor
from .factories import ContributorFactory


class ContributorManagerTestCase(TestCase):
    def test_parse_name_0_words(self):
        parsed = ContributorManager.parse_name('')
        self.assertDictEqual({
            'first_name': '',
            'middle_name': '',
            'last_name': '',
        }, parsed)

    def test_parse_name_1_word(self):
        parsed = ContributorManager.parse_name('Keeno')
        self.assertDictEqual({
            'first_name': '',
            'middle_name': '',
            'last_name': 'Keeno',
        }, parsed)

    def test_parse_name_2_words(self):
        parsed = ContributorManager.parse_name('Edward Sheeran')
        self.assertDictEqual({
            'first_name': 'Edward',
            'middle_name': '',
            'last_name': 'Sheeran',
        }, parsed)

    def test_parse_name_3_words(self):
        parsed = ContributorManager.parse_name('Edward Christopher Sheeran')
        self.assertDictEqual({
            'first_name': 'Edward',
            'middle_name': 'Christopher',
            'last_name': 'Sheeran',
        }, parsed)

    def test_parse_name_4_words(self):
        parsed = ContributorManager.parse_name('Ripoll Shakira Isabel Mebarak')
        self.assertDictEqual({
            'first_name': 'Ripoll',
            'middle_name': 'Shakira Isabel',
            'last_name': 'Mebarak',
        }, parsed)

    def test_match_or_create_match_first_last_name(self):
        c = ContributorFactory(first_name='Elton', last_name='John')
        c1, created = Contributor.objects.match_or_create('Elton John')
        self.assertFalse(created)
        self.assertEqual(c, c1)

    def test_match_or_create_match_last_name(self):
        c = ContributorFactory(first_name='', last_name='Coolio')
        c1, created = Contributor.objects.match_or_create('Coolio')
        self.assertFalse(created)
        self.assertEqual(c, c1)

    def test_match_or_create_create(self):
        c = ContributorFactory(first_name='Justin', last_name='Bieber')
        c1, created = Contributor.objects.match_or_create('Justin Timberlake')
        self.assertTrue(created)
        self.assertNotEqual(c, c1)

    def test_match_or_create_match_and_add_middle_name(self):
        c = ContributorFactory(first_name='Edward', last_name='Sheeran')
        c1, created = Contributor.objects.match_or_create('Edward Christopher Sheeran')
        self.assertFalse(created)

        c.refresh_from_db()
        self.assertEqual(c, c1)
        self.assertEqual('Christopher', c.middle_name)

    def test_match_or_create_mismatch_middle_name(self):
        c = ContributorFactory(first_name='Edward', middle_name='Christopher', last_name='Sheeran')
        c1, created = Contributor.objects.match_or_create('Edward Not-Christopher Sheeran')
        self.assertTrue(created)
        self.assertNotEqual(c, c1)
