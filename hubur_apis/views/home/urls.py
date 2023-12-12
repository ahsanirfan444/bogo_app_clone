from django.urls import path,include
from hubur_apis.views.home import views


from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('all', views.HomeAPIView)
router.register('all_after_have_you_been', views.AfterHaveYouBeenListAPIView)
router.register('all_before_my_fav', views.BeforeMyFavListAPIView)
router.register('all_have_you_been_there', views.HaveYouBeenThereListAPIView)
router.register('all_brands', views.DiscoverBrandListAPIView)
router.register('all_near_by_deals', views.NearByDealsListAPIView)
router.register('all_products_in_offer', views.AllProductsInOfferAPIView)
router.register('all_featured_business', views.AllFeaturedBusinessAPIView)

urlpatterns = [

   path('', include(router.urls)),
   path('view_all_hot_deals/', views.AllProductsInOfferV2APIView.as_view(), name='view-all-hot-deals')
]
