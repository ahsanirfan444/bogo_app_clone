from django.urls import include, path
from hubur_apis.views.reviews import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('create', views.ReviewsView),
router.register('get_products_reviews', views.ReviewsView),
router.register('delete', views.ReviewsView),
router.register('my_reviews', views.ReviewsView),
router.register('update_reviews', views.ReviewsView),
router.register('get_businesses_reviews', views.BusinessReviewsView),

urlpatterns = [

   path('', include(router.urls)),
]
