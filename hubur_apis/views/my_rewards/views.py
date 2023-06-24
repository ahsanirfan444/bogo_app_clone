from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from rest_framework.permissions import IsAuthenticated
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets

from hubur_apis.serializers.reward_serializer import RewardSerializer

class MyRewardListView(viewsets.ModelViewSet):

    queryset = models.UserReward.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):

        next_level_obj = models.Level.objects.filter(type=2).first()
        level_obj = models.Level.objects.filter(type=3).first()
        if level_obj:
            level_name = level_obj.name
            description = level_obj.description
        else:
            level_name = "level 0"
            description = ""

        percentage = 0.0
        
        if next_level_obj:
            next_level_point = next_level_obj.points
            next_level_name = next_level_obj.name
        else:
            next_level_point = 0
            next_level_name = "level 0"
        

        rewards_obj = models.UserReward.objects.filter(i_user=request.user)
        if rewards_obj:
            total_points = int(rewards_obj[0].total_points)
            level_obj = rewards_obj[0].user_level
            level_name = level_obj['name']
            if level_obj['obj']:
                description = level_obj['obj'].description
                next_level_type = int(level_obj['obj'].type) - 1
                
                if next_level_type > 0:
                    next_level_obj = models.Level.objects.filter(type=next_level_type)
                    if next_level_obj:
                        
                        total_next_level_point = int(next_level_obj.first().points)
                        next_level_name = next_level_obj.first().name
                        next_level_point = str(total_next_level_point-total_points) + " points to " + str(next_level_name)
                        percentage = total_points/total_next_level_point
                elif next_level_type == 0:
                    next_level_point = "You have Reached maximum level"
                    percentage = 1.0
            else:
                description = ""
                next_level_point = str(next_level_point-total_points) + " points to " + str(next_level_name)
            
            rewards_obj = self.paginate_queryset(rewards_obj)
            serializer = self.get_serializer(rewards_obj, many=True)
        
            if serializer:
                return Response({'error': [], 'error_code': '','level_name':level_name,"description":description,"next_level_point":next_level_point,"total_point":rewards_obj[0].total_points ,"percentage":percentage,'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
            else:
                next_level_point = str(next_level_point) + " points to " + str(next_level_name)
                return Response({'error': [], 'error_code': '','level_name':level_name,"description":description, "next_level_point":next_level_point, "total_point":0, "percentage":percentage, 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            next_level_point = str(next_level_point) + " points to " + str(next_level_name)
            return Response({'error': [], 'error_code': '','level_name':level_name,"description":description, "next_level_point":next_level_point, "total_point":0, "percentage":percentage, 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)