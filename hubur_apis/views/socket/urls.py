from django.urls import path,include
from hubur_apis.views.socket import views


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('get_data', views.SocketData)
router.register('search_for_map', views.SearchForMapAPIView)
urlpatterns = [

   path('', include(router.urls)),
   path('create_message/', views.CreateMessagesUsingSocket.as_view()),
   path('hit_socket_for_sharing/', views.HitSocketForSharing.as_view()),
]
