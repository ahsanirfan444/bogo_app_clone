from django.urls import include, path
from hubur_apis.views.search import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('all', views.SearchProductAPIView)
router.register('all_v2', views.SearchProductAPIViewV2)  
router.register('popularsearch', views.PopularSearchAPIView)
router.register('all_sub_catagories', views.SubCatagoriesView)
router.register('create_popularsearch', views.PopularSearchAPIView)
router.register('search_for_sub_catagories', views.SearchForSubCatagoriesView)

urlpatterns = [

   path('', include(router.urls)),
]
