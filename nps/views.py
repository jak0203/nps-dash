from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import SurveyAggregations, ClientAggregations, ProductAggregations, ClientDeltas
from .serializers import SurveyAggregationsSerializer
from rest_framework import viewsets


@require_http_methods(['GET'])
@csrf_exempt
def survey_data(request):
    user_type = request.GET.get('users')
    result = SurveyAggregations.objects.filter(user_type=user_type).order_by('survey').values()
    list_result = [entry for entry in result]
    return JsonResponse(list_result, safe=False)


@require_http_methods(['GET'])
@csrf_exempt
def surveys(request):
    result = ClientDeltas.objects.values('survey').order_by('survey').distinct()
    list_result = []
    for entry in result:
        e = entry['survey']
        r = {
            'value': e,
            'display': e,
        }
        list_result.append(r)

    # list_result = [entry['survey'] for entry in result]
    return JsonResponse(list_result, safe=False)



@require_http_methods(['GET'])
@csrf_exempt
def product_data(request):
    product = request.GET.get('product')
    user_type = request.GET.get('users')
    print(product, user_type)
    print(ProductAggregations.objects.filter(user_type=user_type, products=product).count())
    result = ProductAggregations.objects.filter(
        products=product,
        user_type=user_type
    ).order_by('survey').values()
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
    result = ClientAggregations.objects.filter(survey=survey, statistically_significant=True).order_by('-segment').extra(mapping).values(
        'segment', 'promoters', 'neutral', 'detractors', 'nps_score')
    list_result = [entry for entry in result]
    return JsonResponse(list_result, safe=False)


@require_http_methods(['GET'])
@csrf_exempt
def client_deltas(request):
    survey = request.GET.get('survey')
    user_type = request.GET.get('users')
    result = ClientDeltas.objects.filter(survey=survey, user_type=user_type).extra(select={'absolutevalue': 'abs(delta_from_2016)'}).order_by('-absolutevalue').values()
    list_result = [entry for entry in result]
    return JsonResponse(list_result, safe=False)


@require_http_methods(['GET'])
@csrf_exempt
def products(request):
    result = ProductAggregations.objects.values('products').distinct()
    list_result = []
    for entry in result:
        e = entry['products']
        r = {
            'value': e,
            'display': ' & '.join([e[i:i+3] for i in range(0, len(e), 3)]).upper()
        }
        list_result.append(r)
    return JsonResponse(list_result, safe=False)


@require_http_methods(['GET'])
@csrf_exempt
def user_types(request):
    return JsonResponse([
        {
            'value': 'teacher',
            'display': 'Teachers',
        },
        {
            'value': 'non-teacher',
            'display': 'Non-Teachers',
        },
        {
            'value': 'all',
            'display': 'All Users',
        }
    ], safe=False)


class SurveyViewset(viewsets.ModelViewSet):
    queryset = SurveyAggregations.objects.all()
    serializer_class = SurveyAggregationsSerializer

