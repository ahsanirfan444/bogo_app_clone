from django.urls import include, path
from hubur_apis.views.storys import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('business_stories', views.UploadViewSet)
router.register('delete_story', views.DeleteStory)
router.register('user_stories', views.UserStoryViewSet)

urlpatterns = [

   path('', include(router.urls)),
   path('story/<int:pk>', views.ViewSingleStoryView.as_view()),
]
