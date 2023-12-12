
from rest_framework.response import Response
from hubur_apis import models
from rest_framework.views import APIView
from rest_framework import status
import global_methods, notifications
from hubur_apis.serializers.about_serializer import (
    AboutUsUsSerializer, OtherSerializer ,ContactUsSerializer,GetContactUsUsSerializer
)

class AboutUsAPIView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        about_us = models.Other.objects.all()
        serializer = AboutUsUsSerializer(about_us, context={"request": request}, many=True)
        if serializer.data:
            data = serializer.data[0]['about_us']
        else:
            data = ""
        
        return Response({'error': [], 'error_code': '', 'data': data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)


class OtherAPIView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        other = models.Other.objects.all()
        serializer = OtherSerializer(other, context={"request": request}, many=True)
        if serializer.data:
            data = serializer.data[0]
        else:
            data = {}

        return Response({'error': [], 'error_code': '', 'data': data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):

        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            contact_us = models.ContactUs.objects.all()
            if contact_us:
                contact_us = contact_us.first()
                email_address = contact_us.email
                subject = 'Query from %s '% serializer.data['full_name']
                html_message = "Hey, name : %s, contact number : %s, email address : %s, message : %s" % (serializer.data['full_name'], serializer.data['contact'], serializer.data['email'], serializer.data['message'])
                notifications.sendEmailToSingleUser(html_message, email_address, subject)

                return Response({'error': [], 'error_code': '', 'data': ["Email successfully send. We will contact you soon"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                return Response({'error': [], 'error_code': '', 'data': ["No email found by admin"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [serializer.errors], 'error_code': '', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        

class ContactUsAPIView(APIView):
    permission_classes = []
    def get(self, request, *args, **kwargs):
        contact_us = models.ContactUs.objects.all()
        serializer = GetContactUsUsSerializer(contact_us, many=True)
        if serializer.data:
            data = serializer.data[0]
        else:
            data = {}
        
        return Response({'error': [], 'error_code': '', 'data': data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)