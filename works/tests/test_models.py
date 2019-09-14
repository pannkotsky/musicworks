from django.test import TestCase

from works.models import Contributor, Work
from .factories import ContributorFactory, ContributorWorkFactory, WorkFactory


class ContributorTestCase(TestCase):
    def test_full_name_last_name(self):
        contributor = ContributorFactory(first_name='', last_name='Keeno')
        self.assertEqual('Keeno', contributor.full_name())

    def test_full_name_first_last_name(self):
        contributor = ContributorFactory(first_name='Edward', last_name='Sheeran')
        self.assertEqual('Edward Sheeran', contributor.full_name())

    def test_full_name_first_middle_last_name(self):
        contributor = ContributorFactory(first_name='Edward', middle_name='Christopher',
                                         last_name='Sheeran')
        self.assertEqual('Edward Christopher Sheeran', contributor.full_name())

    def test_parse_name_0_words(self):
        first, middle, last = Contributor.parse_name('')
        self.assertEqual('', first)
        self.assertEqual('', middle)
        self.assertEqual('', last)

    def test_parse_name_1_word(self):
        first, middle, last = Contributor.parse_name('Keeno')
        self.assertEqual('', first)
        self.assertEqual('', middle)
        self.assertEqual('Keeno', last)

    def test_parse_name_2_words(self):
        first, middle, last = Contributor.parse_name('Edward Sheeran')
        self.assertEqual('Edward', first)
        self.assertEqual('', middle)
        self.assertEqual('Sheeran', last)

    def test_parse_name_3_words(self):
        first, middle, last = Contributor.parse_name('Edward Christopher Sheeran')
        self.assertEqual('Edward', first)
        self.assertEqual('Christopher', middle)
        self.assertEqual('Sheeran', last)

    def test_parse_name_4_words(self):
        first, middle, last = Contributor.parse_name('Ripoll Shakira Isabel Mebarak')
        self.assertEqual('Ripoll', first)
        self.assertEqual('Shakira Isabel', middle)
        self.assertEqual('Mebarak', last)


class WorkTestCase(TestCase):
    def test_contributors_str(self):
        work = WorkFactory(title='Je ne sais pas')
        ContributorWorkFactory(
            work=work,
            contributor=ContributorFactory(first_name='Obispo', middle_name='Pascal',
                                           last_name='Michel')
        )
        ContributorWorkFactory(
            work=work,
            contributor=ContributorFactory(first_name='Florence', middle_name='Lionel',
                                           last_name='Jacques')
        )
        work = Work.objects.get(pk=work.pk)
        self.assertEqual('Obispo Pascal Michel | Florence Lionel Jacques', work.contributors_str)
