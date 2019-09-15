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


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ['identifier']


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
    newly created Contributor ids, and returns concatenated Contributors' full names for
    output.
    """

    def to_internal_value(self, data):
        contributors = []
        for full_name in data.split('|'):
            contributor_serializer = ContributorSerializer(data={'full_name': full_name})
            contributor_serializer.is_valid(raise_exception=True)
            contributor = contributor_serializer.save()
            contributors.append(contributor.pk)
        return contributors

    def to_representation(self, value):
        return '|'.join(map(str, value.all()))


class DefaultWorkSerializer(serializers.ModelSerializer):
    contributors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Contributor.objects.all())

    class Meta:
        model = Work
        fields = ['iswc', 'source', 'id_from_source', 'title', 'contributors']

    def update(self, instance, validated_data):
        return instance.reconcile(validated_data)


class WorkSerializer(serializers.ModelSerializer):
    # specify field explicitly to disable unique validation
    iswc = serializers.CharField(max_length=11, allow_null=True)
    source = SourceField()
    id = serializers.IntegerField(source='id_from_source')
    contributors = ContributorsField()
    synonyms = serializers.ReadOnlyField(source='synonyms_str')

    class Meta:
        model = Work
        fields = ['iswc', 'source', 'id', 'title', 'synonyms', 'contributors']
        validators = []  # Remove a default "unique together" constraint.

    def create(self, validated_data):
        # Try to get matched instance by data,
        # then delegate validation and creation/update logic to DefaultWorkSerializer
        # Update will happen if instance is None, e.g. nothing matched,
        # creation will happen otherwise

        instance = Work.objects.match(validated_data)
        default_serializer = DefaultWorkSerializer(instance=instance, data=validated_data)
        default_serializer.is_valid(raise_exception=True)
        return default_serializer.save()
