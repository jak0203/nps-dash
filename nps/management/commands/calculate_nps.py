from django.core.management.base import BaseCommand
from nps.models import RawResults, AggregatedResults, SurveyAggregations


STATISTICAL_SIGNIFICANCE = 30


class Command(BaseCommand):
    help = 'Runs the nps calculations and creates the AggregatedResults table.'

    def handle(self, *args, **options):
        # wipe the aggregated results table
        print('Wiping aggregated results')
        AggregatedResults.objects.all().delete()
        SurveyAggregations.objects.all().delete()

        # do the aggregations
        print('doing aggregations')
        for survey in RawResults.objects.values('survey_name').distinct():
            survey_results = {
                'survey_name': survey['survey_name'],
                'total_responses': 0,
                'total_promoters': 0,
                'total_detractors': 0,
                'total_neutral': 0,
                'total_clients': 0,
                'number_clients_positive': 0,
                'number_clients_negative': 0,
            }
            for client in RawResults.objects.filter(survey_name=survey['survey_name']).values('client').distinct():
                score = self.nps(RawResults.objects.filter(
                    survey_name=survey['survey_name'],
                    client=client['client'],
                    question_name='recommend'
                ).distinct())
                score['client'] = client['client']
                score['survey'] = survey['survey_name']
                if score['total_responses'] >= STATISTICAL_SIGNIFICANCE:
                    score['statistically_significant'] = True
                    survey_results['total_clients'] += 1
                    if score['nps_score'] > 0:
                        survey_results['number_clients_positive'] += 1
                    elif score['nps_score'] < 0:
                        survey_results['number_clients_negative'] += 1
                else:
                    score['statistically_significant'] = False
                r = AggregatedResults(**score)
                r.save()

                survey_results['total_responses'] += score['total_responses']
                survey_results['total_promoters'] += score['total_promoters']
                survey_results['total_detractors'] += score['total_detractors']
                survey_results['total_neutral'] += score['total_neutral']
            survey_results['nps_score'] = (survey_results['total_promoters'] - survey_results['total_detractors']) / survey_results['total_responses'] * 100
            survey_results['percent_promoters'] = survey_results['total_promoters']/survey_results['total_responses'] * 100
            survey_results['percent_detractors'] = survey_results['total_detractors'] / survey_results['total_responses'] * 100
            survey_results['percent_neutral'] = survey_results['total_neutral'] / survey_results['total_responses'] * 100
            survey_results['percent_clients_positive'] = survey_results['number_clients_positive'] / survey_results['total_clients'] * 100
            survey_results['percent_clients_negative'] = survey_results['number_clients_negative'] / survey_results['total_clients'] * 100
            survey_results['number_clients_neutral'] = survey_results['total_clients'] - survey_results['number_clients_positive'] - survey_results['number_clients_negative']
            survey_results['percent_clients_neutral'] = survey_results['number_clients_neutral'] / survey_results[
                'total_clients'] * 100
            s = SurveyAggregations(**survey_results)
            s.save()

    def nps(self, data):
        # print('inside aggregate data', data)
        promoters = 0
        detractors = 0
        neutral = 0
        total = 0

        for record in data:
            if int(record.response) in [9, 10]:
                promoters += 1
                total += 1
            elif int(record.response) in [0, 1, 2, 3, 4, 5, 6]:
                detractors += 1
                total += 1
            elif int(record.response) in [7, 8]:
                neutral += 1
                total += 1
        if total == 0:
            score = 0
            print(data.values())
        else:
            score = (promoters - detractors) / total * 100
        return {
            'total_promoters': promoters,
            'total_detractors': detractors,
            'total_neutral': neutral,
            'total_responses': total,
            'percent_promoters': promoters/total * 100,
            'percent_detractors': detractors/total * 100,
            'percent_neutral': neutral/total * 100,
            'nps_score': score
        }


