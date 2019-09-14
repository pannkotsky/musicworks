from django.db.models.manager import Manager


class ContributorManager(Manager):
    @staticmethod
    def parse_name(name):
        """
        Assign name parts from a single string.

        :param name: string containing full name.
        :return: dict of parsed name parts.
        """

        # start with a simplest algorithm
        # ideally some AI-based solution trained on real names should be applied
        # until then new contributors list should be regularly verified by admins
        first_name, middle_name, last_name = '', '', ''
        words = name.split(' ')
        words_count = len(words)
        if words_count == 0:
            pass
        elif words_count == 1:
            last_name = words[0]
        else:
            first_name = ' '.join(words[:1])
            middle_name = ' '.join(words[1:-1])
            last_name = (words[-1])
        return {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
        }

    def match_or_create(self, name):
        """
        Match name to existing contributor or create a new contributor if not matched.

        :param name: string containing full name.
        :return: (instance, created) pair where `instance` is a Contributor and `created` is
                 a boolean indicating whether it was created or matched to existing contributor.
        """

        # assume names are parsed correctly by parse_name(), see note on it above
        # here we don't care about flaws in parsing name parts such as reverse order of names
        # otherwise we can start making lots of extra queries without any quality guarantee
        parsed = self.parse_name(name)

        try:
            instance = self.get(first_name=parsed['first_name'], last_name=parsed['last_name'])
        except (self.model.DoesNotExist, self.model.MultipleObjectsReturned):
            return self.create(**parsed), True

        if parsed['middle_name']:
            if instance.middle_name and instance.middle_name != parsed['middle_name']:
                return self.create(**parsed), True
            if not instance.middle_name:
                instance.middle_name = parsed['middle_name']
                instance.save(update_fields=['middle_name'])
        return instance, False
