from django.urls import include, path
from hubur_apis.views.search import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('all', views.SearchProductAPIView)  
router.register('popularsearch', views.PopularSearchAPIView)
router.register('all_sub_catagories', views.SubCatagoriesView)
router.register('create_popularsearch', views.PopularSearchAPIView)

urlpatterns = [

   path('', include(router.urls)),
]
