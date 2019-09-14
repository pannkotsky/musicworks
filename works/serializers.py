from rest_framework import serializers

from works.models import Work


class WorkSerializer(serializers.ModelSerializer):
    contributors = serializers.ReadOnlyField(source='contributors_str')

    class Meta:
        model = Work
        fields = ['id', 'iswc', 'source', 'id_from_source', 'title', 'contributors']
