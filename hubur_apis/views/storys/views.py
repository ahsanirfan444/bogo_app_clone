from rest_framework.response import Response
from hubur_apis import models
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from hubur_apis.serializers.story_serializer import (
    ImageSerializer
    )

class UploadViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer_class = ImageSerializer(data=request.data, context = {'user_obj':request.user})
        if serializer_class.is_valid():
            serializer_class.save()
            story_obj = serializer_class.instance
            del story_obj['file']
            del story_obj['updated_user']
            if 'image' in story_obj:
                del story_obj['image']
            if 'video' in story_obj:
                del story_obj['video']
            if 'caption' in story_obj:
                del story_obj['caption']
            models.Checkedin.objects.create(**story_obj)
            return Response({'error': '', 'error_code': '', 'data': "Story Uploaded",'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer_class.errors, 'error_code': 'HD404', 'data': "",'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
