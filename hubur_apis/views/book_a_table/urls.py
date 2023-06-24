from django.urls import path
from hubur_apis.views.book_a_table import views


urlpatterns = [

   path('create/',views.BookATableView.as_view({'post':'create'})),
   path('get_all_bookings/',views.BookATableView.as_view({'get': 'list'})),
   
]
