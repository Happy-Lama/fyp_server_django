import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging

cred = credentials.Certificate("firebase-credentials.json")
firebase_admin.initialize_app(cred)


def subscribeUserToNotifications(token):
    response = messaging.subscribe_to_topic(token, 'notification')
    return response.success_count == 1


def send_notification_to_all_users(title, body):
    # topic = 'notification'

    # See documentation on defining a message payload.
    message = messaging.Message(
    notification=messaging.Notification(
            title=title,
            body=body,
        ),
        topic='notification'
    )

    # Send a message to the devices subscribed to the provided topic.
    response = messaging.send(message)
    # Response is a message ID string.
    print('Successfully sent message:', response)
    # return JsonResponse({'message': 'Successfully sent'}, status=200)
    