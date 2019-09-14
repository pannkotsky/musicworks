from django.test import TestCase

from works.models import Work
from .factories import ContributorFactory, ContributorWorkFactory, WorkFactory


class ContributorTestCase(TestCase):
    def test_full_name_last_name(self):
        contributor = ContributorFactory(first_name='', last_name='Keeno')
        self.assertEqual('Keeno', contributor.full_name())
        self.assertEqual('Keeno', str(contributor))

    def test_full_name_first_last_name(self):
        contributor = ContributorFactory(first_name='Edward', last_name='Sheeran')
        self.assertEqual('Edward Sheeran', contributor.full_name())
        self.assertEqual('Edward Sheeran', str(contributor))

    def test_full_name_first_middle_last_name(self):
        contributor = ContributorFactory(first_name='Edward', middle_name='Christopher',
                                         last_name='Sheeran')
        self.assertEqual('Edward Christopher Sheeran', contributor.full_name())
        self.assertEqual('Edward Christopher Sheeran', str(contributor))


class WorkTestCase(TestCase):
    def test_str(self):
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
        self.assertEqual('Je ne sais pas by Obispo Pascal Michel, Florence Lionel Jacques',
                         str(work))
