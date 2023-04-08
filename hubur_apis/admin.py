from django.contrib import admin
from hubur_apis import models
from django.contrib.admin import DateFieldListFilter

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
    list_filter = ('is_active', 'i_day__name',)
    search_fields = ('i_business__name', 'i_business__place_id',)


class ImagesAdmin(admin.ModelAdmin):
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
    search_fields = ('name', 'founded_country', 'founded_year', 'website',)

class CheckInAdmin(admin.ModelAdmin):
    list_filter = ('i_story__is_active',)
    search_fields = ('i_business__name', 'i_business__place_id', 'i_user__first_name', 'i_user__last_name', 'i_story__caption', 'other',)

class ContentAdmin(admin.ModelAdmin):
    list_filter = ('is_active', 'content_type',)
    search_fields = ('name', 'i_business__name', 'i_business__place_id', 'i_user__first_name', 'i_user__last_name', 'i_sub_category__name',)

class DaysAdmin(admin.ModelAdmin):
    list_filter = ('name',)

class OtpAdmin(admin.ModelAdmin):
    list_filter = ('medium',)
    search_fields = ('i_user__first_name', 'i_user__last_name', 'code',)  

class PopularSearchAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ('name', 'type', 'url', 'catagory',)

class RedemptionAdmin(admin.ModelAdmin):
    list_filter = ('is_expired', 'is_redeemed', ('expired_at', DateFieldListFilter),)
    search_fields = ('code', 'i_content__name', 'i_user__first_name', 'i_user__last_name',)

class StoryAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ('caption', 'i_business__name', 'i_business__place_id', 'i_user__first_name', 'i_user__last_name',)

class TrendingDiscountAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
    search_fields = ('name', 'i_business__name', 'i_business__place_id',)

class UserInterestAdmin(admin.ModelAdmin):
    search_fields = ('i_category__name', 'i_user__first_name', 'i_user__last_name',)


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