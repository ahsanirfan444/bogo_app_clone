
from rest_framework.response import Response
from global_methods import get_booking_number
from hubur_apis import models
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status
from core.defaults import DefualtPaginationClass
from hubur_apis.serializers.book_a_table_serializer import (
CreateBookingSerializer,GetAllBookingSerializer
)

class BookATableView(viewsets.ModelViewSet):

    queryset = models.Booking.objects.all()
    pagination_class = DefualtPaginationClass
    serializer_class = CreateBookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = CreateBookingSerializer(data=request.data, context = {'user_obj':request.user})
        if serializer.is_valid():
            serializer.validated_data['i_user'] = request.user
            serializer.validated_data['booking_no'] = get_booking_number()
            
            models.Booking.objects.create(**serializer.validated_data)
            return Response({'error': [], 'error_code': '', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            error_list = []
            for e in serializer.errors.values():
                    error_list.append(e[0])
            return Response({'error': error_list, 'error_code': 'HD404', 'data': [],'status':status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        all_booking = models.Booking.objects.filter(i_user=request.user,i_business__is_active=True).exclude(i_business__i_user__is_active=False)
        all_booking = self.paginate_queryset(all_booking)
        serializer = GetAllBookingSerializer(all_booking,context={"request": request}, many=True)
        
        return Response({'error': [], 'error_code': '', 'data': serializer.data,'status':status.HTTP_200_OK}, status=status.HTTP_200_OK)