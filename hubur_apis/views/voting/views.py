from rest_framework.response import Response
from core.defaults import DefualtPaginationClass
from rest_framework.permissions import IsAuthenticated
from hubur_apis import models
from rest_framework import status
from rest_framework import viewsets
from hubur_apis.serializers.voting_serializer import (
    VotingSerializer,GetAllVotingSerializer,
    )

class VotingView(viewsets.ModelViewSet):

    queryset = models.Voting.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = VotingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer_class = VotingSerializer(data=request.data, context = {'user_obj':request.user})
        if serializer_class.is_valid():
            serializer_class.save()
            voting_obj = serializer_class.instance

            reward_point = models.RewardPoints.objects.filter(type=4)
            if reward_point:
                models.UserReward.objects.create(i_user=request.user, i_business=voting_obj['i_business'], i_point=reward_point[0])
            
            models.Voting.objects.create(**voting_obj)
            return Response({'error': [], 'error_code': '', 'data': ["Voted Successfully"],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer_class.errors.values():
                    error_list.append(e[0])
            return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        user_obj = request.user

        voting_obj = models.Voting.objects.filter(i_user=user_obj)
        voting_obj = self.paginate_queryset(voting_obj)
        vote_serializer = GetAllVotingSerializer(voting_obj,many=True)
        if vote_serializer:
            return Response({'error': [], 'error_code': '', 'data': vote_serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({'error': [], 'error_code': '', 'data': [],'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
             

             
   