from fyp_server.celery import app
from django.utils import timezone
from .models import TransformerData
from notifications.models import Notification
# @app.task
# def hello_world():
#     print("Hello Task is running...")
#     return "Success"

@app.task
def check_off_transformers():

    print("Checking for transformers that have been offline for a period...")

    # get the off-transformers
    off_transformers = TransformerData.objects.off_for_period(duration_minutes=15)

    # find the number of transformers
    number_of_off_transformers = len(off_transformers)

    # save a notification if they exist
    if number_of_off_transformers > 0:
        Notification.objects.create(
            message = f"{number_of_off_transformers} are offline. Check the dashboard",
            notification_type = 'DANGER',
            timestamp = timezone.now()
        )


@app.task
def check_overloaded_transformers():
    print("Checking for transformers that have been overloaded for a period...")

    # find the transformers that have been overloaded for over an 1 hour
    
    # find the number of transformers

    # save a notification if they exist
    
    pass