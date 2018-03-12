from django.db import models

SENTIMENTCHOICES = (
    ('-1', 'Negative'),
    ('0', 'Neutral'),
    ('1', 'Positive'),
    ('', 'Unknown'),
)


class AggregatedResults(models.Model):
    client = models.CharField(max_length=200)
    survey = models.CharField(max_length=200)
    nps_score = models.FloatField()
    percent_detractors = models.FloatField(null=True, blank=True, default=None)
    total_responses = models.IntegerField()
    total_promoters = models.IntegerField()
    percent_promoters = models.FloatField(null=True, blank=True, default=None)
    total_detractors = models.IntegerField()
    total_neutral = models.IntegerField()
    percent_neutral = models.FloatField(null=True, blank=True, default=None)
    statistically_significant = models.BooleanField(default=False)

    class Meta:
        unique_together = ('client', 'survey')


class RawResults(models.Model):
    client = models.CharField(max_length=200)
    survey_name = models.CharField(max_length=200)
    question_type = models.CharField(max_length=30)
    question_name = models.CharField(max_length=30)
    user_id = models.IntegerField()
    response = models.CharField(max_length=500)

    class Meta:
        unique_together = ('client', 'survey_name', 'question_name', 'user_id', 'response')


class Comments(models.Model):
    client = models.CharField(max_length=200)
    survey_name = models.CharField(max_length=200)
    user_id = models.IntegerField()
    response = models.CharField(max_length=500)
    ignore = models.BooleanField(default=False)

    def __str__(self):
        return self.response


class CommentCategories(models.Model):
    category = models.CharField(max_length=30)

    def __str__(self):
        return self.category


class CommentAnalysis(models.Model):
    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE)
    category = models.ForeignKey(CommentCategories, on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=10, choices=SENTIMENTCHOICES)


class SurveyAggregations(models.Model):
    survey_name = models.CharField(max_length=200)

    total_responses = models.IntegerField()
    total_promoters = models.IntegerField()
    percent_promoters = models.FloatField(null=True, blank=True, default=None)
    total_detractors = models.IntegerField()
    percent_detractors = models.FloatField(null=True, blank=True, default=None)
    total_neutral = models.IntegerField()
    percent_neutral = models.FloatField(null=True, blank=True, default=None)

    number_clients_positive = models.IntegerField()
    percent_clients_positive = models.FloatField(null=True, blank=True, default=None)
    number_clients_negative = models.IntegerField()
    percent_clients_negative = models.FloatField(null=True, blank=True, default=None)
    number_clients_neutral = models.IntegerField()
    percent_clients_neutral = models.FloatField(null=True, blank=True, default=None)
    total_clients = models.IntegerField()

    nps_score = models.FloatField(null=True, blank=True, default=None)
