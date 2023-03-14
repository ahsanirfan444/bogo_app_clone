from django.contrib import admin
from hubur_apis import models

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ('role',)
    search_fields = ('email', 'name',)

class BusinessCategoryAdmin(admin.ModelAdmin):
    search_fields = ('name',)

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.OtpToken)
admin.site.register(models.Category, BusinessCategoryAdmin)
admin.site.register(models.SubCategories)
admin.site.register(models.Business)
admin.site.register(models.Images)
admin.site.register(models.Day)
admin.site.register(models.BusinessSchedule)
admin.site.register(models.Banner)
admin.site.register(models.Brand)
admin.site.register(models.Story)
admin.site.register(models.Checkedin)
admin.site.register(models.Content)
admin.site.register(models.ClaimBusiness)
admin.site.register(models.Redemption)
admin.site.register(models.PopularSearch)
admin.site.register(models.UserInterest)