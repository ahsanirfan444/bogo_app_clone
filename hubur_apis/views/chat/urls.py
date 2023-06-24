from django.urls import include, path
from hubur_apis.views.chat  import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('get', views.ChatView),

urlpatterns = [

   path('', include(router.urls)),
   path('create_channel_id/', views.CreateChannelIDView.as_view()),
   path('is_read/', views.IsReadView.as_view()),

]
