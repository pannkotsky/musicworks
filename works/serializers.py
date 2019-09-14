from rest_framework import serializers

from works.models import Work


class WorkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_from_source')
    contributors = serializers.ReadOnlyField(source='contributors_str')

    class Meta:
        model = Work
        fields = ['iswc', 'source', 'id', 'title', 'contributors']
