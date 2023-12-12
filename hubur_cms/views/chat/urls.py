from django.urls import path
from hubur_cms.views.chat import views

urlpatterns = [
    path('', views.all_rooms.as_view(), name="chat"),
    path('user/<user_id>/', views.room_detail.as_view(), name="chat_detail")
]