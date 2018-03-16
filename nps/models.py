from django.db import models

SENTIMENTCHOICES = (
    ('-1', 'Negative'),
    ('0', 'Neutral'),
    ('1', 'Positive'),
    ('', 'Unknown'),
)


class RawResults(models.Model):
    client = models.CharField(max_length=200)
    survey_name = models.CharField(max_length=200)
    question_type = models.CharField(max_length=30)
    question_name = models.CharField(max_length=30)
    user_id = models.IntegerField()
    response = models.CharField(max_length=500)
    can_teach = models.BooleanField(default=False)

    class Meta:
        unique_together = ('client', 'survey_name', 'question_name', 'user_id', 'response')


class ClientAggregations(models.Model):
    client = models.CharField(max_length=30)
    survey = models.CharField(max_length=30)
    user_type = models.CharField(max_length=30, null=True, blank=True, default=None)
    nps_score = models.FloatField(null=True)

    total_responses = models.IntegerField()
    promoters = models.IntegerField()
    detractors = models.IntegerField()
    neutral = models.IntegerField()

    percent_detractors = models.FloatField(null=True, blank=True, default=None)
    percent_promoters = models.FloatField(null=True, blank=True, default=None)
    percent_neutral = models.FloatField(null=True, blank=True, default=None)
    statistically_significant = models.BooleanField(default=False)

    class Meta:
        unique_together = ('client', 'survey', 'user_type')


class SurveyAggregations(models.Model):
    survey = models.CharField(max_length=200)
    user_type = models.CharField(max_length=30, null=True, blank=True, default=None)
    nps_score = models.FloatField(null=True, blank=True, default=None)

    total_responses = models.IntegerField()
    promoters = models.IntegerField()
    detractors = models.IntegerField()
    neutral = models.IntegerField()

    percent_promoters = models.FloatField(null=True, blank=True, default=None)
    percent_detractors = models.FloatField(null=True, blank=True, default=None)
    percent_neutral = models.FloatField(null=True, blank=True, default=None)

    total_clients = models.IntegerField()
    num_clients_positive = models.IntegerField()
    num_clients_negative = models.IntegerField()

    percent_clients_positive = models.FloatField(null=True, blank=True, default=None)
    percent_clients_negative = models.FloatField(null=True, blank=True, default=None)


class Products(models.Model):
    client = models.CharField(max_length=30)
    products = models.CharField(max_length=30)


class ProductAggregations(models.Model):
    survey = models.CharField(max_length=200)
    products = models.CharField(max_length=30)
    user_type = models.CharField(max_length=30, null=True, blank=True, default=None)
    nps_score = models.FloatField(null=True, blank=True, default=None)

    total_responses = models.IntegerField()
    promoters = models.IntegerField()
    detractors = models.IntegerField()
    neutral = models.IntegerField()

    percent_promoters = models.FloatField(null=True, blank=True, default=None)
    percent_detractors = models.FloatField(null=True, blank=True, default=None)
    percent_neutral = models.FloatField(null=True, blank=True, default=None)

    total_clients = models.IntegerField()
    num_clients_positive = models.IntegerField()
    num_clients_negative = models.IntegerField()

    percent_clients_positive = models.FloatField(null=True, blank=True, default=None)
    percent_clients_negative = models.FloatField(null=True, blank=True, default=None)


class ClientDeltas(models.Model):
    client = models.CharField(max_length=30)
    survey = models.CharField(max_length=30)
    products = models.CharField(max_length=30)
    nps_score = models.FloatField(null=True, blank=True, default=None)
    delta_from_2016 = models.FloatField(null=True, blank=True, default=None)
    user_type = models.CharField(max_length=30, null=True, blank=True, default=None)
    statistically_significant_delta = models.BooleanField(default=False)


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



