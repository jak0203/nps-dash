from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import SurveyAggregations, AggregatedResults, ProductAggregations
from .serializers import SurveyAggregationsSerializer
from rest_framework import viewsets


@require_http_methods(['GET'])
@csrf_exempt
def survey_data(request):
    mapping = {
        'segment': 'survey_name',
        'promoters': 'percent_promoters',
        'neutral': 'percent_neutral',
        'detractors': 'percent_detractors',
        # 'nps_score': round('nps_score', 2),
    }
    result = SurveyAggregations.objects.extra(mapping).values(
        'segment', 'promoters', 'neutral', 'detractors', 'nps_score')
    list_result = [entry for entry in result]
    return JsonResponse(list_result, safe=False)


@require_http_methods(['GET'])
@csrf_exempt
def client_data(request):
    survey = request.GET.get('survey')

    mapping = {
        'segment': 'client',
        'promoters': 'percent_promoters',
        'neutral': 'percent_neutral',
        'detractors': 'percent_detractors',
    }
    result = AggregatedResults.objects.filter(survey=survey, statistically_significant=True).order_by('-segment').extra(mapping).values(
        'segment', 'promoters', 'neutral', 'detractors', 'nps_score')
    list_result = [entry for entry in result]
    return JsonResponse(list_result, safe=False)


@require_http_methods(['GET'])
@csrf_exempt
def product_data(request):
    product = request.GET.get('product')
    mapping = {
        'segment': 'survey_name',
        'promoters': 'percent_promoters',
        'neutral': 'percent_neutral',
        'detractors': 'percent_detractors'
    }
    result = ProductAggregations.objects.filter(products=product).order_by('segment').extra(mapping).values(
        'segment', 'promoters', 'neutral', 'detractors', 'nps_score', 'total_responses'
    )
    list_result = [entry for entry in result]
    return JsonResponse(list_result, safe=False)

class SurveyViewset(viewsets.ModelViewSet):
    queryset = SurveyAggregations.objects.all()
    serializer_class = SurveyAggregationsSerializer
