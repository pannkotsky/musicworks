from django.test import TestCase

from works.models import Contributor, Work
from .factories import ContributorFactory, ContributorWorkFactory, WorkFactory


class ContributorManagerTestCase(TestCase):
    def test_parse_name_0_words(self):
        parsed = Contributor.objects.parse_name('')
        self.assertDictEqual({
            'first_name': '',
            'middle_name': '',
            'last_name': '',
        }, parsed)

    def test_parse_name_1_word(self):
        parsed = Contributor.objects.parse_name('Keeno')
        self.assertDictEqual({
            'first_name': '',
            'middle_name': '',
            'last_name': 'Keeno',
        }, parsed)

    def test_parse_name_2_words(self):
        parsed = Contributor.objects.parse_name('Edward Sheeran')
        self.assertDictEqual({
            'first_name': 'Edward',
            'middle_name': '',
            'last_name': 'Sheeran',
        }, parsed)

    def test_parse_name_3_words(self):
        parsed = Contributor.objects.parse_name('Edward Christopher Sheeran')
        self.assertDictEqual({
            'first_name': 'Edward',
            'middle_name': 'Christopher',
            'last_name': 'Sheeran',
        }, parsed)

    def test_parse_name_4_words(self):
        parsed = Contributor.objects.parse_name('Ripoll Shakira Isabel Mebarak')
        self.assertDictEqual({
            'first_name': 'Ripoll',
            'middle_name': 'Shakira Isabel',
            'last_name': 'Mebarak',
        }, parsed)

    def test_match_or_create_match_first_last_name(self):
        c = ContributorFactory(first_name='Elton', last_name='John')
        c1, created = Contributor.objects.match_or_create('Elton JOHN')
        self.assertFalse(created)
        self.assertEqual(c, c1)

    def test_match_or_create_match_last_name(self):
        c = ContributorFactory(first_name='', last_name='Coolio')
        c1, created = Contributor.objects.match_or_create('coolio')
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

    def test_match_or_create_match_middle_name_case_insensitive(self):
        c = ContributorFactory(first_name='Edward', middle_name='christopher', last_name='Sheeran')
        c1, created = Contributor.objects.match_or_create('Edward Christopher Sheeran')
        self.assertFalse(created)

        c.refresh_from_db()
        self.assertEqual(c, c1)
        self.assertEqual('christopher', c.middle_name)

    def test_match_or_create_mismatch_middle_name(self):
        c = ContributorFactory(first_name='Edward', middle_name='Christopher', last_name='Sheeran')
        c1, created = Contributor.objects.match_or_create('Edward Not-Christopher Sheeran')
        self.assertTrue(created)
        self.assertNotEqual(c, c1)


class WorkManagerTestCase(TestCase):
    def test_match_by_iswc(self):
        work = WorkFactory(iswc='T0000000033')
        matched = Work.objects.match({
            'iswc': 'T0000000033',
            'source': 'warner',
            'id_from_source': 1,
            'title': 'Hello',
            'contributors': [],
        })
        self.assertEqual(work, matched)

    def test_match_by_source_iswc_in_data(self):
        work = WorkFactory(iswc=None)
        matched = Work.objects.match({
            'iswc': 'T0000000033',
            'source': work.source,
            'id_from_source': work.id_from_source,
            'title': 'Hello',
            'contributors': [],
        })
        self.assertEqual(work, matched)

    def test_not_match_by_source_if_different_iswc(self):
        work = WorkFactory(iswc='T0000000032')
        matched = Work.objects.match({
            'iswc': 'T0000000033',
            'source': work.source,
            'id_from_source': work.id_from_source,
            'title': 'Hello',
            'contributors': [],
        })
        self.assertIsNone(matched)

    def test_match_by_title_and_contributor(self):
        work = WorkFactory(iswc=None)
        ContributorWorkFactory.create_batch(3, work=work)
        matched = Work.objects.match({
            'iswc': 'T0000000033',
            'source': 'warner',
            'id_from_source': 1,
            'title': work.title,
            'contributors': [work.contributors.all()[0], ContributorFactory()],
        })
        self.assertEqual(work, matched)

    def test_not_match_by_title_and_contributor_if_different_iswc(self):
        work = WorkFactory(iswc='T0000000032')
        ContributorWorkFactory.create_batch(3, work=work)
        matched = Work.objects.match({
            'iswc': 'T0000000033',
            'source': 'warner',
            'id_from_source': 1,
            'title': work.title,
            'contributors': [work.contributors.all()[0], ContributorFactory()],
        })
        self.assertIsNone(matched)

    def test_match_by_source_if_title_and_contributor_also_matches(self):
        """
        Check that if source and id_from_source matches one Work instance and title+contributor
        matches other Work instance, source match will be returned.
        """

        work1 = WorkFactory(iswc=None)
        work2 = WorkFactory(iswc=None)
        ContributorWorkFactory.create_batch(3, work=work2)
        matched = Work.objects.match({
            'iswc': 'T0000000033',
            'source': work1.source,
            'id_from_source': work1.id_from_source,
            'title': work2.title,
            'contributors': [work2.contributors.all()[0], ContributorFactory()],
        })
        self.assertEqual(work1, matched)

    def test_match_by_source_no_iswc_in_data(self):
        work = WorkFactory(iswc='T0000000032')
        matched = Work.objects.match({
            'iswc': None,
            'source': work.source,
            'id_from_source': work.id_from_source,
            'title': 'Hello',
            'contributors': [],
        })
        self.assertEqual(work, matched)

    def test_match_by_title_and_contributor_no_iswc_in_data(self):
        work = WorkFactory(iswc='T0000000032')
        ContributorWorkFactory.create_batch(3, work=work)
        matched = Work.objects.match({
            'iswc': None,
            'source': 'warner',
            'id_from_source': 1,
            'title': work.title,
            'contributors': [work.contributors.all()[0], ContributorFactory()],
        })
        self.assertEqual(work, matched)

    def test_match_by_source_if_title_and_contributor_also_matches_no_iswc_in_data(self):
        """
        Check that if source and id_from_source matches one Work instance and title+contributor
        matches other Work instance, source match will be returned.
        """

        work1 = WorkFactory()
        work2 = WorkFactory()
        ContributorWorkFactory.create_batch(3, work=work2)
        matched = Work.objects.match({
            'iswc': None,
            'source': work1.source,
            'id_from_source': work1.id_from_source,
            'title': work2.title,
            'contributors': [work2.contributors.all()[0], ContributorFactory()],
        })
        self.assertEqual(work1, matched)
