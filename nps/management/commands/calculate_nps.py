from django.core.management.base import BaseCommand
from nps.models import RawResults, ClientAggregations, SurveyAggregations

# these variables are also imported into calculate_nps_product.py
STATISTICAL_SIGNIFICANCE = 30
SURVEYS = {
    'February 2018 NPS Survey': '2018 February',
    'Test Survey': '2016 April',
    'November 2017 NPS Survey': '2017 November',
}
USER_TYPES = {
    'teacher': True,
    'non-teacher': False
}
COUNT_TYPES = ['total_responses', 'promoters', 'detractors', 'neutral']


def nps(data):
    if data['total_responses'] == 0:
        return 0
    return round((data['promoters'] - data['detractors']) / data['total_responses'] * 100, 2)


def nps_counts(data):
    total = 0
    promoters = 0
    detractors = 0
    neutral = 0
    totals = {}

    for record in data:
        if int(record.response) in [9, 10]:
            promoters += 1
        elif int(record.response) in [1, 2, 3, 4, 5, 6]:
            detractors += 1
        else:
            neutral += 1
        total += 1

        if total == 0:
            totals['nps_score'] = 0
            print(data.values())
        else:
            totals['nps_score'] = round((promoters - detractors) / total * 100, 2)

    totals['promoters'] = promoters
    totals['detractors'] = detractors
    totals['neutral'] = neutral
    totals['total_responses'] = total
    # validate data before returning
    assert (totals['promoters'] + totals['detractors'] + totals['neutral'] == totals['total_responses'])
    return totals


def statistically_significant(total):
    if total >= STATISTICAL_SIGNIFICANCE:
        return True
    return False


def calculate_percentages(data):
    # Calculate the percentages and round to 2 decimal places - ensure they all add to 100%
    percentages = {}
    if data['total_responses'] == 0:
        percentages['percent_promoters'] = 0
        percentages['percent_detractors'] = 0
        percentages['percent_neutral'] = 0
        return percentages

    percentages['percent_promoters'] = round(data['promoters'] / data['total_responses'] * 100, 2)
    percentages['percent_detractors'] = round(data['detractors'] / data['total_responses'] * 100, 2)
    percentages['percent_neutral'] = round(data['neutral'] / data['total_responses'] * 100, 2)
    # determine difference from 100 and add to the smallest as-needed
    delta = 100 - (
            percentages['percent_promoters'] + percentages['percent_detractors'] + percentages['percent_neutral']
    )
    percentages['percent_neutral'] += round(delta, 2)
    return percentages


def calculate_client_percentages(data):
    percentages = {}
    if data['total_clients'] == 0:
        percentages['percent_clients_positive'] = 0
        percentages['percent_clients_negative'] = 0
        return percentages
    percentages['percent_clients_positive'] = round(data['num_clients_positive'] / data['total_clients'] * 100, 2)
    percentages['percent_clients_negative'] = round(data['num_clients_negative'] / data['total_clients'] * 100, 2)
    delta = 100 - (
            percentages['percent_clients_positive'] + percentages['percent_clients_negative']
    )
    percentages['percent_clients_positive'] += round(delta, 2)
    return percentages


class Command(BaseCommand):
    help = 'Runs the nps aggregations and creates the AggregatedResults table.'

    def handle(self, *args, **options):
        # wipe aggregated results table
        print('Wiping aggregated results')
        ClientAggregations.objects.all().delete()
        SurveyAggregations.objects.all().delete()

        # get list of surveys
        for survey_raw_name, survey_clean_name in SURVEYS.items():
            survey_results_raw = {
                'all': {
                    'survey': survey_clean_name,
                    'user_type': 'all',
                    'total_responses': 0,
                    'promoters': 0,
                    'detractors': 0,
                    'neutral': 0,
                    'num_clients_positive': 0,
                    'num_clients_negative': 0,
                    'total_clients': 0,
                }
            }
            for user_type in USER_TYPES.keys():
                survey_results_raw[user_type] = {
                    'survey': survey_clean_name,
                    'user_type': user_type,
                    'total_responses': 0,
                    'promoters': 0,
                    'detractors': 0,
                    'neutral': 0,
                    'num_clients_positive': 0,
                    'num_clients_negative': 0,
                    'total_clients': 0,
                }
            for client in RawResults.objects.filter(survey_name=survey_raw_name).values('client').distinct():
                client_results_raw = {
                    'client': client['client'],
                    'survey': survey_clean_name,
                    'user_type': 'all',
                    'total_responses': 0,
                    'promoters': 0,
                    'detractors': 0,
                    'neutral': 0,
                }
                for user_type, can_teach in USER_TYPES.items():
                    print(survey_raw_name, client)
                    querycount = RawResults.objects.filter(
                        survey_name=survey_raw_name,
                        client=client['client'],
                        can_teach=can_teach,
                        question_name='recommend'
                    ).distinct().count()
                    if querycount == 0:
                        continue
                    user_results_raw = nps_counts(RawResults.objects.filter(
                        survey_name=survey_raw_name,
                        client=client['client'],
                        can_teach=can_teach,
                        question_name='recommend'
                    ).distinct())
                    user_results_percentages = calculate_percentages(user_results_raw)
                    user_results = {
                        'survey': survey_clean_name,
                        'client': client['client'],
                        'user_type': user_type,
                        'statistically_significant': statistically_significant(user_results_raw['total_responses']),
                        **user_results_raw,
                        **user_results_percentages,
                    }
                    r = ClientAggregations(**user_results)
                    r.save()
                    # add results to total
                    for count_type in COUNT_TYPES:
                        survey_results_raw[user_type][count_type] += user_results[count_type]
                        client_results_raw[count_type] += user_results[count_type]

                    if user_results['statistically_significant'] is True:
                        survey_results_raw[user_type]['total_clients'] += 1
                        if user_results_raw['nps_score'] >= 0:
                            survey_results_raw[user_type]['num_clients_positive'] += 1
                        else:
                            survey_results_raw[user_type]['num_clients_negative'] += 1

                client_results_percentages = calculate_percentages(client_results_raw)
                client_results = {
                    **client_results_raw,
                    **client_results_percentages,
                    'nps_score': nps(client_results_raw),
                    'statistically_significant': statistically_significant(client_results_raw['total_responses'])
                }
                r = ClientAggregations(**client_results)
                r.save()

                for count_type in COUNT_TYPES:
                    survey_results_raw['all'][count_type] += client_results[count_type]

                if client_results['statistically_significant'] is True:
                    survey_results_raw['all']['total_clients'] += 1
                    if client_results['nps_score'] >= 0:
                        survey_results_raw['all']['num_clients_positive'] += 1
                    else:
                        survey_results_raw['all']['num_clients_negative'] += 1

            for user_type in USER_TYPES.keys():
                survey_results = {
                    **survey_results_raw[user_type],
                    'nps_score': nps(survey_results_raw[user_type]),
                    **calculate_percentages(survey_results_raw[user_type]),
                    **calculate_client_percentages(survey_results_raw[user_type]),
                }
                r = SurveyAggregations(**survey_results)
                r.save()
            survey_results = {
                **survey_results_raw['all'],
                'nps_score': nps(survey_results_raw['all']),
                **calculate_percentages(survey_results_raw['all']),
                **calculate_client_percentages(survey_results_raw['all']),
            }
            r = SurveyAggregations(**survey_results)
            r.save()




