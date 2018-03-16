from django.core.management.base import BaseCommand
from .calculate_nps import STATISTICAL_SIGNIFICANCE, SURVEYS, USER_TYPES, COUNT_TYPES, \
    nps, calculate_percentages, calculate_client_percentages
from nps.models import ClientAggregations, ProductAggregations, Products


class Command(BaseCommand):
    help = 'Runs the nps calculations and creates the AggregatedResults table.'

    def handle(self, *args, **options):
        # wipe the results table
        print('Wiping aggregated results')
        ProductAggregations.objects.all().delete()

        products = Products.objects.values('products').distinct()

        for survey_raw_name, survey_clean_name in SURVEYS.items():
            for product in products:
                for user_type in USER_TYPES:
                    product_results_raw = {
                        'survey': survey_clean_name,
                        'user_type': user_type,
                        'products': product['products'],
                        'total_responses': 0,
                        'promoters': 0,
                        'detractors': 0,
                        'neutral': 0,
                        'num_clients_positive': 0,
                        'num_clients_negative': 0,
                        'total_clients': 0,
                    }

                    print(product, survey_raw_name, user_type)
                    for client in ClientAggregations.objects.filter(
                        survey=survey_clean_name,
                        user_type=user_type,
                        client__in=Products.objects.filter(products=product['products']).values('client')
                    ):
                        for count_type in COUNT_TYPES:
                            product_results_raw[count_type] += getattr(client, count_type)
                        if client.statistically_significant is True:
                            product_results_raw['total_clients'] += 1
                            if client.nps_score >= 0:
                                product_results_raw['num_clients_positive'] += 1
                            else:
                                product_results_raw['num_clients_negative'] += 1
                    # calculate percentages and nps for the user type
                    product_results = {
                        **product_results_raw,
                        'nps_score': nps(product_results_raw),
                        **calculate_percentages(product_results_raw),
                        **calculate_client_percentages(product_results_raw),
                    }
                    # print(product_results)
                    r = ProductAggregations(**product_results)
                    r.save()
