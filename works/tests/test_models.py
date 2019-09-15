from django.test import TestCase

from works.models import Work
from .factories import ContributorFactory, SourceFactory, WorkFactory


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
        work = WorkFactory(title='Je ne sais pas', contributors=[
            ContributorFactory(first_name='Obispo', middle_name='Pascal', last_name='Michel'),
            ContributorFactory(first_name='Florence', middle_name='Lionel', last_name='Jacques')
        ])
        work = Work.objects.get(pk=work.pk)
        self.assertEqual('Je ne sais pas by Obispo Pascal Michel, Florence Lionel Jacques',
                         str(work))

    def test_reconcile_update_name_and_contributors(self):
        c1 = ContributorFactory(first_name='John', middle_name='Edward', last_name='O Brien')
        c2 = ContributorFactory(first_name='Thomas', middle_name='Edward', last_name='Yorke')
        c3 = ContributorFactory(first_name='James', middle_name='Philip', last_name='Selway')
        work = WorkFactory(title='Adventure of lifetime', contributors=[c1, c2])
        updated = work.reconcile({
            'iswc': work.iswc,
            'title': 'Adventure of A Lifetime',
            'contributors': [c2, c3],
            'source': SourceFactory(identifier='warner'),
            'id_from_source': 3,
        })
        self.assertEqual('Adventure of lifetime', updated.title)
        self.assertListEqual(['Adventure of A Lifetime'], updated.title_synonyms)
        self.assertCountEqual([c1, c2, c3], updated.contributors.all())
        self.assertEqual('warner', updated.source.identifier)
        self.assertEqual(3, updated.id_from_source)
