from django.conf import settings
from push_notifications.models import WebPushDevice, GCMDevice
from core.base import AuthBaseViews
from hubur_apis import models
from constants import HOME_ACTIVITIES_OF_ANDROID, HOME_ACTIVITIES_OF_IOS
import os, json
from firebase_admin import messaging, credentials
import firebase_admin 
import sendgrid
from sendgrid.helpers.mail import *
from django.db.models import Q
from datetime import timedelta
from twilio.rest import Client
from push_notifications.webpush import WebPushError
from global_methods import pause_notifications_promotional_messages, pause_all_notifications, pause_notifications_new_offer, pause_notifications_offer_expire


def sendNotificationToSingleUser(userID, msg, msg_ar, title, title_ar, sender_id, content_id, action,notification_type=None, activityAndroid=None, activityIOS=None, code=None, **kwargs):
    """Method to send notification to single user."""
    try:
        
        notificationSaved = False
        pause_notifications1 = pause_all_notifications([userID])
        pause_notifications2 = pause_notifications_offer_expire([userID],notification_type)
        pause_notifications3 = []
        pause_notifications4 = pause_notifications_new_offer([userID],notification_type)
        
        gcm = GCMDevice.objects.filter(user_id=userID, active__in=[True]).exclude(Q(user_id__in=pause_notifications1) | Q(user_id__in=pause_notifications2) |
            Q(user_id__in=pause_notifications3) | Q(user_id__in=pause_notifications4)).order_by('-date_created')[:1]
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
                    if user_instance.lang_code == 1:
                        resp = sendAndroidMessage(title=title, body=msg, activityAndroid=None, activityIOS=None, data=kwargs, token=d.registration_id)
                    else:
                        resp = sendAndroidMessage(title=title_ar, body=msg_ar, activityAndroid=None, activityIOS=None, data=kwargs, token=d.registration_id)
                except Exception as e:
                    raise e
                    resp = None
                    pass

                if resp is not None and not isinstance(resp, list) and not notificationSaved:
                    if user_instance.lang_code == 1:
                        models.Notification.objects.create(user=user_instance, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action, code=code)
                        notificationSaved = True
                    else:
                        models.Notification.objects.create(user=user_instance, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action, code=code)
                        notificationSaved = True
                else:
                    if user_instance.lang_code == 1:
                        models.Notification.objects.create(user=user_instance, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action, code=code)
                        notificationSaved = True
                    else:
                        models.Notification.objects.create(user=user_instance, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action, code=code)
                        notificationSaved = True
                print("Response: ", resp)

        else:
            if user_instance.lang_code == 1:
                models.Notification.objects.create(user=user_instance, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action, code=code)
                notificationSaved = True
            else:
                models.Notification.objects.create(user=user_instance, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action, code=code)
                notificationSaved = True

    except Exception as e:
        print(e)
        pass
    return


def sendNotificationToMultipleUser(userIDs, msg, msg_ar, title, title_ar, sender_id, content_id, action,notification_type=None, activityAndroid=None, activityIOS=None, **kwargs):
    """Method to send notification to multiple users"""

    if not firebase_admin._apps:
        cred = credentials.Certificate(os.path.join(settings.BASE_DIR, "keys", "serviceAccountKey.json")) 
        default_app = firebase_admin.initialize_app(cred)

    sentNotificationIDs = []
    excluded_user_id = []
    if pause_all_notifications(userIDs):
        excluded_user_id.extend(pause_all_notifications(userIDs))
    else:
        if pause_notifications_promotional_messages(userIDs):
            excluded_user_id.extend(pause_notifications_promotional_messages(userIDs))

        if pause_notifications_new_offer(userIDs, notification_type):
            excluded_user_id.extend(pause_notifications_new_offer(userIDs,notification_type))

        if pause_notifications_offer_expire(userIDs, notification_type):
            excluded_user_id.extend(pause_notifications_offer_expire(userIDs,notification_type))
    gcm = GCMDevice.objects.filter(user_id__in=userIDs, active__in=[True]).exclude(user_id__in=excluded_user_id).order_by('-date_created')[:1]

    sender_instance = models.UserProfile.objects.get(id=sender_id)
    user_instances = models.UserProfile.objects.filter(id__in=userIDs)

    if gcm:
        for d in gcm:
            if activityAndroid is None:
                activityAndroid = HOME_ACTIVITIES_OF_ANDROID[str(d.user.role)]
            if activityIOS is None:
                activityIOS = HOME_ACTIVITIES_OF_IOS[str(d.user.role)]
            try:
                if d.user.lang_code == 1:
                    resp = sendAndroidMessage(title=title, body=msg, activityAndroid=None, activityIOS=None, data=kwargs, token=d.registration_id)
                else:
                    resp = sendAndroidMessage(title=title_ar, body=msg_ar, activityAndroid=None, activityIOS=None, data=kwargs, token=d.registration_id)
            except Exception as e:
                resp = None
                pass
            
            if d.user != sender_instance:
                if resp is not None and d.user.id not in sentNotificationIDs:
                    if d.user.lang_code == 1:
                        models.Notification.objects.create(user=d.user, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action)
                        sentNotificationIDs.append(d.user.id)
                    else:
                        models.Notification.objects.create(user=d.user, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action)
                        sentNotificationIDs.append(d.user.id)
                else:
                    if d.user.lang_code == 1:
                        models.Notification.objects.create(user=d.user, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action)
                        sentNotificationIDs.append(d.user.id)
                    else:
                        models.Notification.objects.create(user=d.user, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action)
                        sentNotificationIDs.append(d.user.id)
                    
                print("Return Response: ", resp)

    else:
        for user in user_instances:
            if user != sender_instance:
                if user.lang_code == 1:
                    models.Notification.objects.create(user=user, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action)
                    sentNotificationIDs.append(user)
                else:
                    models.Notification.objects.create(user=user, sender=sender_instance, notification_type=notification_type, content_id=content_id, title=title, title_ar=title_ar, body=msg, body_ar=msg_ar, action=action)
                    sentNotificationIDs.append(user)

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


def sendMessageToSingleUser(msg, user_id):
    """ Method to send sms through user_id """
    if settings.DEBUG:
        client = Client(settings.TWILLIO_ACCOUNT_SID, settings.TWILLIO_AUTH_TOKEN)
        try:
            user = models.UserProfile.objects.get(id=user_id)
            contact = user.country_code + user.contact
        except models.UserProfile.DoesNotExist:
            return False
        msg = msg + f"\n\n{AuthBaseViews.SITE_TITLE} Team"
        try:
            client.messages.create(to=contact, from_=settings.TWILLIO_NUMBER, body=msg)
        except Exception as e:
            print(e)
            pass
    return


def sendMessageToMultipleUsers(msg, user_ids):
    """Method to send SMS to multiple users. This method will receive list of user ids to send SMS"""
    if settings.DEBUG:
        users = models.UserProfile.objects.filter(id__in=user_ids)
        client = Client(settings.TWILLIO_ACCOUNT_SID, settings.TWILLIO_AUTH_TOKEN)
        msg = msg + f"\n{AuthBaseViews.SITE_TITLE} Team"
        for user in users:
            contact = user.country_code + user.contact
            try:
                client.messages.create(to=contact, from_=settings.TWILLIO_NUMBER, body=msg)
            except Exception:
                pass

    return


def sendNotificationToAdmin(msg, title, sender_id, notification_type, redirectURL, content_id=None):
    """Method to send notification to Admin"""

    sentNotificationIDs = []
    data = json.dumps({"title": title, "message": msg, "tag": "StandardNotify", "url": redirectURL})
    wp = WebPushDevice.objects.filter(user__role=3, active=True)
    if wp.exists():
        for device in wp:
            try:
                resp = device.send_message(data)
                if resp is not None and device.user.id not in sentNotificationIDs:
                    models.Notification.objects.create(user=device.user, sender_id=sender_id, notification_type=notification_type, content_id=content_id, title=title, body=msg, action=None)
                    sentNotificationIDs.append(device.user.id)
                print("Admin response: ", resp)
            except WebPushError as e:
                print(e)
                pass
    else:
        user_instance = models.UserProfile.objects.filter(role=3).first()
        models.Notification.objects.create(user=user_instance, sender_id=sender_id, notification_type=notification_type, content_id=content_id, title=title, body=msg, action=None)

    return


def sendNotificationToVendor(userID, msg, title, sender_id, notification_type, redirectURL):
    """Method to send notification to Vendor"""

    sentNotificationIDs = []
    data = json.dumps({"title": title, "message": msg, "tag": "StandardNotify", "url": redirectURL})
    wp = WebPushDevice.objects.filter(user_id=userID, user__role=2, active=True)
    if wp.exists():
        for device in wp:
            try:
                resp = device.send_message(data)
                if resp is not None and device.user.id not in sentNotificationIDs:
                    models.Notification.objects.create(user=device.user, sender_id=sender_id, notification_type=notification_type, content_id=None, title=title, body=msg, action=None)
                    sentNotificationIDs.append(device.user.id)
                print("Vendor response: ", resp)
            except WebPushError as e:
                print(e)
                pass
    else:
        models.Notification.objects.create(user_id=userID, sender_id=sender_id, notification_type=notification_type, content_id=None, title=title, body=msg, action=None)

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