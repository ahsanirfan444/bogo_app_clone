from django.conf import settings
from push_notifications.models import WebPushDevice, GCMDevice
from hubur_apis import models
from constants import HOME_ACTIVITIES_OF_ANDROID, HOME_ACTIVITIES_OF_IOS
import os
from firebase_admin import messaging, credentials
import firebase_admin 
import sendgrid
from sendgrid.helpers.mail import *
from datetime import timedelta
from twilio.rest import Client


def sendNotificationToSingleUser(userID, msg, title, sender_id, content_id, action,notification_type=None, activityAndroid=None, activityIOS=None, **kwargs):
    """Method to send notification to single user."""
    try:
        notificationSaved = False
        gcm = GCMDevice.objects.filter(user_id=userID, active__in=[True]).order_by('-date_created')[:1]
        if not firebase_admin._apps:
            cred = credentials.Certificate(os.path.join(settings.BASE_DIR, "keys", "serviceAccountKey.json")) 
            default_app = firebase_admin.initialize_app(cred)

        sender_instance = models.UserProfile.objects.get(id=sender_id)
        user_instance = models.UserProfile.objects.get(id=userID)

        if gcm:
            for d in gcm:
                if activityAndroid is None:
                    activityAndroid = HOME_ACTIVITIES_OF_ANDROID[str(d.user.role)]
                if activityIOS is None:
                    activityIOS = HOME_ACTIVITIES_OF_IOS[str(d.user.role)]
                try:
                    resp = sendAndroidMessage(title=title, body=msg, activityAndroid=None, activityIOS=None, data=kwargs, token=d.registration_id)
                except Exception as e:
                    raise e
                    resp = None
                    pass

                if resp is not None and not isinstance(resp, list) and not notificationSaved:
                    models.Notification.objects.create(user=user_instance, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, body=msg, action=action)
                    notificationSaved = True
                else:
                    models.Notification.objects.create(user=user_instance, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, body=msg, action=action)
                    notificationSaved = True
                print("Response: ", resp)

        else:
            models.Notification.objects.create(user=user_instance, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, body=msg, action=action)
            notificationSaved = True

    except Exception as e:
        print(e)
        pass
    return


def sendNotificationToMultipleUser(userIDs, msg, title, sender_id, content_id, action,notification_type=None, activityAndroid=None, activityIOS=None, **kwargs):
    """Method to send notification to multiple users"""

    if not firebase_admin._apps:
        cred = credentials.Certificate(os.path.join(settings.BASE_DIR, "keys", "serviceAccountKey.json")) 
        default_app = firebase_admin.initialize_app(cred)

    sentNotificationIDs = []
    gcm = GCMDevice.objects.filter(user_id__in=userIDs, active__in=[True])

    sender_instance = models.UserProfile.objects.get(id=sender_id)
    user_instances = models.UserProfile.objects.filter(id__in=userIDs)

    if gcm:
        for d in gcm:
            if activityAndroid is None:
                activityAndroid = HOME_ACTIVITIES_OF_ANDROID[str(d.user.role)]
            if activityIOS is None:
                activityIOS = HOME_ACTIVITIES_OF_IOS[str(d.user.role)]
            try:
                resp = sendAndroidMessage(title=title, body=msg, activityAndroid=None, activityIOS=None, data=kwargs, token=d.registration_id)
            except Exception as e:
                resp = None
                pass
            
            if d.user != sender_instance:
                if resp is not None and d.user.id not in sentNotificationIDs:
                    models.Notification.objects.create(user=d.user, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, body=msg, action=action)
                    sentNotificationIDs.append(d.user.id)
                else:
                    models.Notification.objects.create(user=d.user, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, body=msg, action=action)
                    sentNotificationIDs.append(d.user.id)
                    
                print("Return Response: ", resp)

    else:
        for user in user_instances:
            if user != sender_instance:
                models.Notification.objects.create(user=user, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, body=msg, action=action)
                sentNotificationIDs.append(user.id)

    return



def sendEmailToSingleUser(body, to, subject):
    """Method to send Email to single User"""

    sg = sendgrid.SendGridAPIClient(api_key=settings.EMAIL_HOST_PASSWORD)
    from_email = Email(settings.DEFAULT_FROM_EMAIL)
    to_email = To(to)
    content = Content("text/html", body)
    mail = Mail(from_email, to_email, subject, content)
    try:
        sg.client.mail.send.post(request_body=mail.get())
    except Exception as e:
        print(e)
        pass
    
    return

def sendSMSToSingleUser(body, to):
    """Method to send SMS to single User"""

    try:
        client = Client(settings.TWILLIO_ACCOUNT_SID, settings.TWILLIO_AUTH_TOKEN)
        client.messages.create(body=body,
            from_=settings.TWILLIO_NUMBER,
            to=to
        )
    except:
        pass
    
    return


def getJsonResponse(data, status):
    """This method will return the custom json response"""

    resp = {
        "status": status,
        "data": data
    }

    return resp


def sendAndroidMessage(title, body, activityAndroid, activityIOS, token, data={}):
    """This method will setup fcm messages"""

    alert = messaging.ApsAlert(title = title, body = body)
    aps = messaging.Aps(alert = alert, category=activityIOS, sound="default")
    payload = messaging.APNSPayload(aps)

    message = messaging.Message(
        notification = messaging.Notification(
            title = title,
            body = body
        ),
        data=data,
        android=messaging.AndroidConfig(
            ttl=timedelta(seconds=3600),
            priority='high',
            notification=messaging.AndroidNotification(
                title=title,
                body=body,
                click_action = activityAndroid
            ),
            data=data,
        ),
        apns = messaging.APNSConfig(payload = payload),
        token=token,
    )

    response = messaging.send(message)
    
    return response