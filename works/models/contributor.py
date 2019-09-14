from django.db import models


class Contributor(models.Model):
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    middle_name = models.CharField(max_length=100, blank=True, default='')
    # should be set to true when correctness of name parts is verified
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return ' '.join(filter(lambda x: x, (self.first_name, self.middle_name, self.last_name)))

    @staticmethod
    def parse_name(name):
        """
        Assign name parts from a single string.

        :param name: string containing full name.
        :return: tuple (first_name, middle_name, last_name) - parsed name parts.
        """

        # start with a simplest algorithm
        # ideally some AI-based solution trained on real names should be applied
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
        return first_name, middle_name, last_name
