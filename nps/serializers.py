
from rest_framework import serializers

from .models import SurveyAggregations


class SurveyAggregationsSerializer(serializers.HyperlinkedModelSerializer):
    segment = serializers.CharField(source='survey_name')
    promoters = serializers.FloatField(source='percent_promoters')
    neutral = serializers.FloatField(source='percent_neutral')
    detractors = serializers.FloatField(source='percent_detractors')

    class Meta:
        model = SurveyAggregations
        fields = ('segment', 'promoters', 'neutral', 'detractors')

