from django.core.management.base import BaseCommand
from .calculate_nps import STATISTICAL_SIGNIFICANCE, SURVEYS, USER_TYPES, COUNT_TYPES, \
    nps, calculate_percentages, calculate_client_percentages
from nps.models import ClientAggregations, ProductAggregations, Products, ClientDeltas


class Command(BaseCommand):
    help = 'Runs calculations for client deltas.'

    def handle(self, *args, **options):
        # wipe the table
        ClientDeltas.objects.all().delete()

        for survey_raw_name, survey_clean_name in SURVEYS.items():
            for user_type in USER_TYPES.keys():
                for client in ClientAggregations.objects.filter(
                        survey=survey_clean_name,
                        user_type=user_type,
                        statistically_significant=True,
                ).values():
                    p = Products.objects.filter(client=client['client']).values('products')
                    print(client['client'], p[0])
                    results = {
                        'client': client['client'],
                        'nps_score': client['nps_score'],
                        'products': p[0]['products'],
                        'survey': survey_clean_name,
                        'user_type': user_type,
                    }
                    if survey_clean_name in ('2018 February', '2017 November'):
                        nps_2016 = ClientAggregations.objects.filter(
                            survey='2016 April', user_type=user_type, client=client['client']
                        ).values()
                        if nps_2016.count() > 0:
                            results['delta_from_2016'] = results['nps_score'] - nps_2016[0]['nps_score']
                            if (nps_2016[0]['statistically_significant'] >= STATISTICAL_SIGNIFICANCE) and (
                                    client['statistically_signficant'] >= STATISTICAL_SIGNIFICANCE):
                                results['statistically_significant'] = True
                    r = ClientDeltas(**results)
                    r.save()
