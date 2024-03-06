from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from notifications.serializers import NotificationSerializer
from notifications.models import Notification
from api.models import TransformerSpecification, TransformerData
from api.serializers import TransformerDataSerializer
from datetime import timedelta
from django.utils import timezone

# from django.db.models import Max

def index(request):
    transformer_latest_data = TransformerDataSerializer().get_latest_data()
    return JsonResponse({"latest_data": transformer_latest_data}, status=200)

def get_notifications(request, filter):
    # get the latest notifications
    notifications = Notification.objects.all()
    if filter == 'all':
        return JsonResponse({'notifications': NotificationSerializer(notifications, many=True).data})
    if filter == 'latest':
        notifications = notifications.order_by('-timestamp')[:100]
        return JsonResponse({'notifications': NotificationSerializer(notifications, many=True).data})
    
def get_overall_transformer_data(request):
    # get data for the summary statistics page
    # average percentage loading of the transformers over period of one day
    # min loading, and its associated transformer
    # max loading, and its associated transformer
    # number of transformers that are off
    # number of overloaded transformers
    # number of on transformers
    # number of registered transformers
    # max output frequency, and its associated transformer
    # min output frequency, and its associated transformer
    # average frequency
    # max output voltage, and its associated transformer
    # min output voltage and its associated transformer
    # average output voltage
    results = TransformerDataSerializer().get_overall_data()

    return JsonResponse({'overall_stats': results}, status=200)

def moving_time_average_data(request):
    # get data for the summary statistics graphs
    # this is the overall transformer data but in time windows
    # watching the min, average and max loading over time period of 1 week
    # more data to be considered
    startTime = timezone.now() - timedelta(days=7) #adjust for new timeframes
    interval = 60
    results = TransformerDataSerializer().moving_average(startTime, interval)

    return JsonResponse({'data': results}, status=200)

def register_transformer(request):
    # register new transformer specifications
    if request.method == 'POST':
        # implement error handling
        request_data = request.POST
        
        transformer = TransformerSpecification.objects.create(
            transformer_id=request_data['devUID'],
            latitude=request_data['latitude'],
            longitude=request_data['longitude'],
            power_rating=request_data['nominal_power_rating'],
            transformer_type=request_data['type']
        )

        return JsonResponse({'message': 'Transformer Registered'}, status=200)
    else:
        return JsonResponse({'message': 'Method Not Allowed'}, status=405)

def get_transformer_data(request, transformer_id):
    # get individual transformer data to be plotted
    data = TransformerDataSerializer().transformer_data(transformer_id)
    return JsonResponse({'data': data}, status=200)
    # pass