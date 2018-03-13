from django.core.management.base import BaseCommand
from nps.models import RawResults, AggregatedResults, SurveyAggregations, ProductAggregations, Products

STATISTICAL_SIGNIFICANCE = 30


class Command(BaseCommand):
    help = 'Runs the nps calculations and creates the AggregatedResults table.'

    def handle(self, *args, **options):
        # wipe the results table
        ProductAggregations.objects.all().delete()

        products = Products.objects.values('products').distinct()
        print(products)

        # do the aggregations
        for survey in RawResults.objects.values('survey_name').distinct():
            print(survey['survey_name'])
            # don't hard code survey names
            if survey['survey_name'] == 'Test Survey':
                s = '2016 April'
            elif '2017' in survey['survey_name']:
                s = '2017 November'
            elif '2018' in survey['survey_name']:
                s = '2018 February'
            product_results = {}
            for product in products:
                product_results = {
                    'survey_name': s,
                    'products': product['products'],
                    'total_responses': 0,
                    'total_promoters': 0,
                    'total_detractors': 0,
                    'total_neutral': 0,
                    'total_clients': 0,
                    'number_clients_positive': 0,
                    'number_clients_negative': 0,
                }
                client_data = AggregatedResults.objects.filter(
                    survey=s,
                    client__in=Products.objects.filter(products=product['products']).values('client')
                )
                for client in client_data:
                    product_results['total_responses'] += client.total_responses
                    product_results['total_detractors'] += client.total_detractors
                    product_results['total_promoters'] += client.total_promoters
                    product_results['total_neutral'] += client.total_neutral

                    if client.statistically_significant == True:
                        product_results['total_clients'] += 1
                        if client.nps_score > 0:
                            product_results['number_clients_positive'] += 1
                        elif client.nps_score < 0:
                            product_results['number_clients_negative'] += 1
                if product_results['total_responses'] != 0:
                    product_results['nps_score'] = round((product_results['total_promoters'] - product_results['total_detractors']) / product_results['total_responses'] * 100, 2)
                    product_results['percent_promoters'] = product_results['total_promoters'] / product_results[
                        'total_responses'] * 100
                    product_results['percent_detractors'] = product_results['total_detractors'] / product_results[
                        'total_responses'] * 100
                    product_results['percent_neutral'] = product_results['total_neutral'] / product_results[
                        'total_responses'] * 100
                product_results['number_clients_neutral'] = product_results['total_clients'] - product_results[
                    'number_clients_positive'] - product_results['number_clients_negative']
                if product_results['total_clients'] != 0:
                    product_results['percent_clients_positive'] = product_results['number_clients_positive'] / product_results[
                        'total_clients'] * 100
                    product_results['percent_clients_negative'] = product_results['number_clients_negative'] / product_results[
                        'total_clients'] * 100

                    product_results['percent_clients_neutral'] = product_results['number_clients_neutral'] / product_results[
                        'total_clients'] * 100

                p = ProductAggregations(**product_results)
                p.save()
