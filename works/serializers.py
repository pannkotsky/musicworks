from rest_framework import serializers

from works.models import Contributor, Source, Work


class ContributorSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = Contributor
        fields = ['id', 'full_name', 'first_name', 'middle_name', 'last_name', 'verified']
        read_only_fields = ['id', 'first_name', 'middle_name', 'last_name', 'verified']

    def create(self, validated_data):
        full_name = validated_data.pop('full_name')
        contributor, created = Contributor.objects.match_or_create(full_name)
        return contributor


class SourceField(serializers.CharField):
    """
    Field that converts string input into existing or newly created Source object
    and returns Source's identifier for output.
    """

    def to_internal_value(self, data):
        source, created = Source.objects.get_or_create(identifier=data)
        return source

    def to_representation(self, value):
        return value.identifier


class ContributorsField(serializers.CharField):
    """
    Field that converts string of concatenated contributors names into list of existing and/or
    newly created Contributor objects, and returns concatenated Contributors' full names for
    output.
    """

    def to_internal_value(self, data):
        contributors = []
        for full_name in data.split('|'):
            contributor_serializer = ContributorSerializer(data={'full_name': full_name})
            contributor_serializer.is_valid(raise_exception=True)
            contributor = contributor_serializer.save()
            contributors.append(contributor)
        return contributors

    def to_representation(self, value):
        return '|'.join(map(str, value.all()))


class WorkSerializer(serializers.ModelSerializer):
    source = SourceField()
    id = serializers.IntegerField(source='id_from_source')
    contributors = ContributorsField()

    class Meta:
        model = Work
        fields = ['iswc', 'source', 'id', 'title', 'contributors']
