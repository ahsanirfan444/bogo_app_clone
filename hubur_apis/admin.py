from django.contrib import admin
from hubur_apis import models
from django.contrib.admin import DateFieldListFilter

from hubur_cms.forms.admin_form import BusinessAdminForm

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ('role', 'is_verified', 'is_type', 'is_active',)
    search_fields = ('email', 'first_name', 'last_name', 'country_code', 'contact',)

class BusinessCategoryAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ('name',)

class BusinessSubCategoryAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ('name', 'i_category__name',)

class BusinessAdmin(admin.ModelAdmin):
    list_filter = ('is_claimed', 'i_category', 'i_subcategory',)
    search_fields = ('name', 'place_id',)

class BusinessScheduleAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    list_filter = ('is_active', 'i_day__name',)
    search_fields = ('i_business__name', 'i_business__place_id',)


class ImagesAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    list_filter = ('is_active', 'type',)
    search_fields = ('i_business__name', 'i_business__place_id', 'i_user__first_name', 'i_user__last_name',)


class ClaimBusinessAdmin(admin.ModelAdmin):
    list_filter = ('approve',)
    search_fields = ('i_business__name', 'i_business__place_id', 'business_email', 'trade_license_number',)


class BannerAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'position', )
    search_fields = ('i_user__first_name', 'i_user__last_name', 'i_subcatagory__name',)

class BrandsAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ('name', 'website',)

class CheckInAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    list_filter = ('i_story__is_active',)
    search_fields = ('i_business__name', 'i_business__place_id', 'i_user__first_name', 'i_user__last_name', 'i_story__caption', 'other',)

class ContentAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    list_filter = ('is_active', 'content_type',)
    search_fields = ('name', 'i_business__name', 'i_business__place_id', 'i_user__first_name', 'i_user__last_name', 'i_sub_category__name',)

class DaysAdmin(admin.ModelAdmin):
    list_filter = ('name',)

class OtpAdmin(admin.ModelAdmin):
    list_filter = ('medium',)
    search_fields = ('i_user__first_name', 'i_user__last_name', 'code',)  

class PopularSearchAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    list_filter = ('is_active',)
    search_fields = ('^i_business__name', 'i_brand__name','type',)

class RedemptionAdmin(admin.ModelAdmin):
    list_filter = ('is_expired', 'is_redeemed', ('expired_at', DateFieldListFilter),)
    search_fields = ('code', 'i_content__name', 'i_user__first_name', 'i_user__last_name',)

class StoryAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    list_filter = ('is_active',)
    search_fields = ('caption', 'i_business__name', 'i_business__place_id', 'i_user__first_name', 'i_user__last_name',)

class TrendingDiscountAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    list_filter = ('is_active',)
    search_fields = ('name', 'i_business__name', 'i_business__place_id',)

class UserInterestAdmin(admin.ModelAdmin):
    search_fields = ('i_category__name', 'i_user__first_name', 'i_user__last_name',)

class VotingAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    search_fields = ( 'i_business__name', 'vote','i_user__first_name', 'i_user__last_name',)

class FavAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    search_fields = ( 'i_business__name','i_user__first_name', 'i_user__last_name',)

class VistedAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    search_fields = ( 'i_business__name','i_user__first_name', 'i_user__last_name',)

class FAQAdmin(admin.ModelAdmin):
    search_fields = ( 'question','answer',)

class BookingAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    list_filter = ('status',)
    search_fields = ( 'i_business__name','i_user__first_name', 'i_user__last_name',)

class CountryAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ( 'name',)

class CityAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ( 'name', 'i_country__name',)

class MyBookmarkAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    search_fields = ( 'i_business__name', 'vote','i_user__first_name', 'i_user__last_name',)

class OffersAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    list_filter = ('is_expiry', 'is_active', 'type', 'discount_type', ('start', DateFieldListFilter), ('end', DateFieldListFilter),)
    search_fields = ( 'i_business__name','i_user__first_name', 'i_user__last_name', 'name',)

class AttributesAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ( 'name', 'value',)

class ReviewsAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    search_fields = ( 'review', 'i_business__name','i_content__name')

class NotificationAdmin(admin.ModelAdmin):
    list_filter = ('reviewed',)
    search_fields = ('sender__first_name', 'user__last_name', 'title',)

class SavedOffersAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    search_fields = ( 'i_content__name', 'i_business__name','i_user__first_name', 'i_user__last_name')

class FriendListAdmin(admin.ModelAdmin):
    search_fields = ('i_user__first_name', 'i_user__last_name',)

class RewardPointsAdmin(admin.ModelAdmin):
    search_fields = ('type', 'points',)

class UserRewardAdmin(admin.ModelAdmin):
    form = BusinessAdminForm
    search_fields = ('i_user__first_name', 'i_user__last_name','i_business__name')

class MessageAdmin(admin.ModelAdmin):
    search_fields = ('sender__first_name', 'sender__last_name','receiver__first_name', 'receiver__last_name','content','channel_id',)

class ChatAdmin(admin.ModelAdmin):
    search_fields = ('user_1__first_name', 'user_1__last_name','user_2__first_name', 'user_2__last_name','channel_id',)

class LevelAdmin(admin.ModelAdmin):
    search_fields = ('name', 'type',)

class UserOnlineStatusAdmin(admin.ModelAdmin):
    search_fields = ('i_user__first_name', 'i_user__last_name','is_online',)

admin.site.site_header = 'Hubur Database Administration'

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.OtpToken, OtpAdmin)
admin.site.register(models.Category, BusinessCategoryAdmin)
admin.site.register(models.SubCategories, BusinessSubCategoryAdmin)
admin.site.register(models.Business, BusinessAdmin)
admin.site.register(models.Images, ImagesAdmin)
admin.site.register(models.Day, DaysAdmin)
admin.site.register(models.BusinessSchedule, BusinessScheduleAdmin)
admin.site.register(models.Banner, BannerAdmin)
admin.site.register(models.Brand, BrandsAdmin)
admin.site.register(models.Story, StoryAdmin)
admin.site.register(models.Checkedin, CheckInAdmin)
admin.site.register(models.Content, ContentAdmin)
admin.site.register(models.ClaimBusiness, ClaimBusinessAdmin)
admin.site.register(models.Redemption, RedemptionAdmin)
admin.site.register(models.PopularSearch, PopularSearchAdmin)
admin.site.register(models.UserInterest, UserInterestAdmin)
admin.site.register(models.TrendingDiscount, TrendingDiscountAdmin)
admin.site.register(models.Voting, VotingAdmin)
admin.site.register(models.MyFavourite, FavAdmin)
admin.site.register(models.Visited, VistedAdmin)
admin.site.register(models.FAQ, FAQAdmin)
admin.site.register(models.Other)
admin.site.register(models.ContactUs)
admin.site.register(models.Booking, BookingAdmin)
admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.City, CityAdmin)
admin.site.register(models.MyBookmark, MyBookmarkAdmin)
admin.site.register(models.Offers, OffersAdmin)
admin.site.register(models.Attributes, AttributesAdmin)
admin.site.register(models.Reviews, ReviewsAdmin)
admin.site.register(models.Notification, NotificationAdmin)
admin.site.register(models.SavedOffers, SavedOffersAdmin)
admin.site.register(models.FriendList, FriendListAdmin)
admin.site.register(models.RewardPoints, RewardPointsAdmin)
admin.site.register(models.UserReward, UserRewardAdmin)
admin.site.register(models.Level, LevelAdmin)
admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.Chat, ChatAdmin)
admin.site.register(models.UserOnlineStatus, UserOnlineStatusAdmin)