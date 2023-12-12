import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from global_methods import file_size
from django.urls import reverse_lazy

# Create your models here.


class UserProfileManager(BaseUserManager):

    def create_user(self, username,first_name,last_name, email,country_code, gender, i_country, i_city, contact, lang_code=1, terms_conditions=None , is_type = None,dob = None, address= None, password=None, profile_picture=None):

        if not any([ username,first_name,last_name,email]):
            raise ValueError(
                "[ name, last_name, email all fields are required")

        email = self.normalize_email(email=email)

        user = self.model(username=username,first_name=first_name,last_name=last_name, email=email, country_code=country_code, gender=gender, i_country=i_country, i_city=i_city, contact=contact, lang_code=lang_code, is_type=is_type, dob=dob, address=address, profile_picture=profile_picture, terms_conditions=terms_conditions)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, gender, email, password=None):

        user = self.create_user(username, gender, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICE = (
        (1, "Male"),
        (2, "Female"),
    )
    ROLE_CHOICE = (
        (1, "User"),
        (2, "Vendor"),
        (3, "Admin"),
        (4, "Super User")
    )

    IS_TYPE_CHOICE = (
        (1, "Normal"),
        (2, "Social")
    )

    IS_LANGUAGE_CODE = (
        (1, "English"),
        (2, "Arabic")
    )

    username = models.CharField(max_length=30, blank=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.IntegerField(choices=GENDER_CHOICE, default=1, null=True, blank=True)
    email = models.EmailField(max_length=50, unique=True)
    role = models.IntegerField(choices=ROLE_CHOICE, default=1)
    is_active = models.BooleanField(default=False)
    is_type = models.IntegerField(choices=IS_TYPE_CHOICE, default=1)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    contact = models.CharField(max_length=15, unique=True)
    country_code = models.CharField(max_length=5)
    i_city = models.ForeignKey('hubur_apis.City', on_delete=models.CASCADE, null=True, blank=True)
    i_country = models.ForeignKey('hubur_apis.Country', on_delete=models.CASCADE, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=225,null=True,blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", default='profile_pictures/logo_min.png', null=True, blank=True)
    bg_image = models.ImageField(upload_to="profile_pictures/", default='profile_pictures/default_user_bg.jpg')
    long = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    terms_conditions = models.BooleanField(default=False)
    subscription = models.ForeignKey('hubur_apis.UserSubscription', on_delete=models.CASCADE, null=True, blank=True)
    lang_code = models.IntegerField(choices=IS_LANGUAGE_CODE, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def get_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f"{self.get_name()} | {self.email} | {self.country_code}-{self.contact} | {self.lang_code}"

    def is_user(self):
        return self.role == 1

    def is_vendor(self):
        return self.role == 2
    
    def is_admin(self):
        return self.role == 3

    def is_superuser(self):
        return self.role == 4
    
    @property
    def get_profile_percentage(self):
        if self.is_admin():
            rate = 3
            if self.get_name() == "" or self.get_name() == None:
                rate -= 1
            if self.dob == "" or self.dob == None:
                rate -= 1
            if self.profile_picture == "" or self.profile_picture == "profile_pictures/logo_min.png" or self.profile_picture == None:
                rate -= 1
            
            return round((rate/3)*100)
        
        if self.is_vendor():
            rate = 7
            if self.get_name() == "" or self.get_name() == None:
                rate -= 1
            if self.dob == "" or self.dob == None:
                rate -= 1
            if self.profile_picture == "" or self.profile_picture == "profile_pictures/logo_min.png" or self.profile_picture == None:
                rate -= 1
            if Images.objects.filter(i_user=self.id).count() < 10:
                rate -= 1
            
            try:
                business_instance = Business.objects.get(i_user=self.id)
                if business_instance.website == "" or business_instance.website == None:
                    rate -= 1

                if business_instance.logo_pic == "" or business_instance.logo_pic == "business_images/bag.png" or business_instance.logo_pic == None:
                    rate -= 1

                if BusinessSchedule.objects.filter(~models.Q(start_time=None), i_business=business_instance.id).count() < 7:
                    rate -= 1

            except Business.DoesNotExist:
                pass
            
            return round((rate/7)*100)
    

    class Meta:
        db_table = 'Users'
        ordering = ['-created_at']
        verbose_name_plural = "Users"



class OtpToken(models.Model):
    SMS = '1'
    EMAIL = '2'
    MEDIUM_CHOICE = (
        (SMS, "SMS"),
        (EMAIL, "Email")
    )
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    medium = models.CharField(choices=MEDIUM_CHOICE, max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.i_user.get_name()} | {self.i_user.email} | {self.code}"

    class Meta:
        db_table = 'otp_token'
        ordering = ['-created_at']
        verbose_name_plural = "Otp Codes"


class Country(models.Model):
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'country'
        ordering = ['name']
        verbose_name_plural = "Countries"


class City(models.Model):
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, null=True)
    i_country = models.ForeignKey('hubur_apis.Country', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name} | {self.i_country.name}'

    class Meta:
        db_table = 'city'
        ordering = ['name']
        verbose_name_plural = "Cities"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    name_ar = models.CharField(max_length=255, unique=True, null=True)
    image = models.ImageField(upload_to="category_images/", null=True,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_edit_url(self):
        return reverse_lazy("edit_category", kwargs={"cat_id": self.id})

    class Meta:
        db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = "Categories"


class SubCategories(models.Model):
    name = models.CharField(max_length=255, unique=True)
    name_ar = models.CharField(max_length=255, unique=True, null=True)
    image = models.ImageField(upload_to="category_images/", null=True,blank=True)
    i_category = models.ForeignKey('hubur_apis.Category', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_edit_url(self):
        return reverse_lazy("edit_sub_category", kwargs={"sub_cat_id": self.id})
    
    def get_delete_url(self):
        return reverse_lazy("delete_sub_category", kwargs={"pk": self.id})

    class Meta:
        db_table = 'sub_categories'
        ordering = ['-created_at']
        verbose_name_plural = "Sub Categories"

class Business(models.Model):
    IS_CLAIM_CHOICE = (
        (1, "No"),
        (2, "Yes")
    )
    name = models.CharField(max_length=255)
    about = models.TextField(default="")
    contact = models.CharField(max_length=15)
    country_code = models.CharField(max_length=5)
    address = models.CharField(max_length=255)
    long = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    logo_pic = models.ImageField(upload_to="business_images/", default='business_images/bag.png')
    i_category = models.ForeignKey('hubur_apis.Category', on_delete=models.CASCADE)
    i_subcategory = models.ManyToManyField('hubur_apis.SubCategories')
    i_attributes = models.ManyToManyField('hubur_apis.Attributes', null=True, blank=True)
    i_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    is_claimed = models.IntegerField(choices=IS_CLAIM_CHOICE, default=1)
    is_featured = models.BooleanField(default=False)
    place_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.i_user:
            return f"{self.name} | {self.i_category.name} | {self.i_user.get_name()} | {self.get_is_claimed_display()}"
        else:
            return f"{self.name} | {self.i_category.name} | {self.get_is_claimed_display()}"

    class Meta:
        db_table = 'business_db'
        ordering = ['-updated_at']
        verbose_name_plural = "Businesses"


class Content(models.Model):
    CONTENT_TYPE_CHOICE = (	
        (1, "Product"),	
        (2, "Service"),	
        (3, "Menu"),	
        (4, "Health Care"),	
    )
    name = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, null=True)
    description = models.TextField()
    description_ar = models.TextField(null=True)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.IntegerField(choices=CONTENT_TYPE_CHOICE, default=1)
    i_sub_category = models.ForeignKey('hubur_apis.SubCategories', on_delete=models.CASCADE, null=True, blank=True)
    i_brand = models.ForeignKey('hubur_apis.Brand', on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    sku = models.CharField(max_length=15, null=True, blank=True)
    color = models.CharField(max_length=10, null=True, blank=True)
    code = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.i_sub_category.name} | {self.price} | {self.i_user.get_name()} | {self.is_active}"

    def get_edit_product_url(self):
        return reverse_lazy("edit_products", kwargs={"content_id": self.id})
    
    def get_delete_product_url(self):
        return reverse_lazy("delete_products", kwargs={"pk": self.id})
    
    def get_edit_service_url(self):
        return reverse_lazy("edit_services", kwargs={"content_id": self.id})
    
    def get_delete_service_url(self):
        return reverse_lazy("delete_services", kwargs={"pk": self.id})
    
    def get_edit_health_care_service_url(self):
        return reverse_lazy("edit_health_care_services", kwargs={"content_id": self.id})
    
    def get_delete_health_care_service_url(self):
        return reverse_lazy("delete_health_care_services", kwargs={"pk": self.id})
    
    def get_edit_menu_url(self):
        return reverse_lazy("edit_menu", kwargs={"content_id": self.id})
    
    def get_delete_menu_url(self):
        return reverse_lazy("delete_menu", kwargs={"pk": self.id})
    
    class Meta:
        db_table = 'contents'
        ordering = ['-created_at']
        verbose_name_plural = "Contents"

class ClaimBusiness(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)
    business_email = models.EmailField(max_length=50, unique=True)
    trade_license_number = models.CharField(max_length=50)
    trade_license = models.FileField(upload_to="trade_license/", validators=[file_size])
    approve = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} | {self.first_name} | {self.last_name} | {self.i_business.name} | {self.business_email}"

    def get_claim_approve_url(self):
        return reverse_lazy("approve_claim_business", kwargs={"claim_id": self.pk})
    
    def get_claim_reject_url(self):
        return reverse_lazy("reject_claim_business", kwargs={"claim_id": self.pk})
    
    def extension(self):
        name, extension = os.path.splitext(self.trade_license.name)
        return extension
    
    class Meta:
        db_table = 'claim_business_db'
        ordering = ['-created_at']
        verbose_name_plural = "Claim Business"
        


class Images(models.Model):
    TYPE_CHOICE = (	
        (1, "Business_Catalog"),
        (2, "Product"),
        (3, "Service"),
        (4, "Menu"),	
        (5, "Health Care"),	
    )
    type = models.IntegerField(choices=TYPE_CHOICE)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE, null=True, blank=True)
    i_content = models.ForeignKey('hubur_apis.Content', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="other_images/")
    is_active = models.BooleanField(default=True)
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.i_user.get_name()} | {self.is_active}"
    
    def get_edit_url(self):
        return reverse_lazy("edit_business_catalogue", kwargs={"cat_id": self.id})
    
    def get_delete_url(self):
        return reverse_lazy("delete_business_catalogue", kwargs={"pk": self.id})

    class Meta:
        db_table = 'images'
        ordering = ['-created_at']
        verbose_name_plural = "Images"


class Day(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'days'
        ordering = ['-created_at']
        verbose_name_plural = "Days"


class BusinessSchedule(models.Model):
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)
    i_day = models.ForeignKey('hubur_apis.Day', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.i_business.name} | {self.i_day.name}"

    class Meta:
        db_table = 'business_schedule'
        ordering = ['-created_at']
        verbose_name_plural = "Business Schedule"


class Banner(models.Model):
    POSITION_CHOICE = (
        (1, "Top"),
        (2, "Middle"),
        (3, "After Have You Been There"),
        (4, "Before My Favourites"),
        (5, "Category Page"),
        (6, "Bottom"),
        (7, "Top Hot"),
        (8, "Middle Hot"),
    )

    PLATFORM_CHOICE = (
        (1, "Mobile"),
        (2, "Web")
    )	

    POSITION_CHOICE_AR = (
        (1, "قمة"),
        (2, "وسط"),
        (3, "بعد أن كنت هناك"),
        (4, "قبل المفضلة"),
        (5, "صفحة الفئة"),
        (6, "قاع"),
        (7, "توب هوت"),
        (8, "وسط حار"),
    )

    PLATFORM_CHOICE_AR = (
        (1, "متحرك"),
        (2, "الويب")
    )

    LANGUAGE_CHOICE = (
        (1, "English"),
        (2, "العربية")
    )
    
    image = models.ImageField(upload_to="banner_images/", null=True, blank=True)	
    position = models.IntegerField(choices=POSITION_CHOICE)	
    platform = models.IntegerField(choices=PLATFORM_CHOICE)	
    language = models.IntegerField(choices=LANGUAGE_CHOICE)	
    i_subcatagory = models.ForeignKey('hubur_apis.SubCategories', on_delete=models.CASCADE, null=True, blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} | {self.i_user.get_name()} | {self.is_active}"
    
    def get_edit_url(self):
        return reverse_lazy("edit_banners", kwargs={"ban_id": self.id})
    
    def get_delete_url(self):
        return reverse_lazy("delete_banners", kwargs={"pk": self.id})

    class Meta:
        db_table = 'banner_db'
        ordering = ['-created_at']
        verbose_name_plural = "Banners"


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    name_ar = models.CharField(max_length=255, unique=True, null=True)
    image = models.ImageField(upload_to="brand_images/")
    website = models.URLField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.is_active}"
    
    def get_edit_url(self):
        return reverse_lazy("edit_brands", kwargs={"brand_id": self.id})
    
    def get_delete_url(self):
        return reverse_lazy("delete_brands", kwargs={"pk": self.id})

    class Meta:
        db_table = 'brand_db'
        ordering = ['-created_at']
        verbose_name_plural = "Brands"


class Story(models.Model):
    caption = models.CharField(max_length=255, null=True,blank=True)
    video = models.FileField(upload_to="story_videos/", validators=[file_size], null=True,blank=True)
    image = models.ImageField(upload_to="story_images/", null=True,blank=True)
    is_active = models.BooleanField(default=True)
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    updated_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE, related_name="updated_user")
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} | {self.i_user.get_name()} | {self.i_business.name} | {self.is_active}"
    
    def get_deactivate_url(self):
        return reverse_lazy("vendor_deactivate_stories", kwargs={"story_id": self.id})
    
    def get_delete_url(self):
        return reverse_lazy("vendor_delete_stories", kwargs={"pk": self.id})

    class Meta:
        db_table = 'story_db'
        ordering = ['-created_at']
        verbose_name_plural = "Stories"


class Checkedin(models.Model):
    i_story = models.ForeignKey('hubur_apis.Story', on_delete=models.CASCADE, null=True, blank=True)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    other = models.CharField(max_length=255, null=True, blank=True)
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} | {self.i_user.get_name()} | {self.i_business.name}"

    class Meta:
        db_table = 'checked_in_db'
        ordering = ['-created_at']
        verbose_name_plural = "Check In's"


class Redemption(models.Model):
    
    code = models.CharField(max_length=255)
    i_content = models.ForeignKey('hubur_apis.Content', on_delete=models.CASCADE)
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    is_redeemed  = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    expired_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} | {self.i_user.get_name()} | {self.is_redeemed} | {self.is_expired}"

    class Meta:
        db_table = 'redemption_db'
        ordering = ['-created_at']
        verbose_name_plural = "Redemptions"


class PopularSearch(models.Model):
    i_brand = models.ForeignKey('hubur_apis.Brand', on_delete=models.CASCADE, null=True, blank=True)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE, null=True, blank=True)
    i_content = models.ForeignKey('hubur_apis.Content', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    count = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.i_business:
            return f"{self.i_business.name} | {self.count} | {self.type} | {self.is_active}"
        elif self.i_content:
            return f"{self.i_content.name} | {self.count} | {self.type} | {self.is_active}"
        else:
            return f"{self.i_brand.name} | {self.count} | {self.type} | {self.is_active}"

    class Meta:
        db_table = 'popular_search_db'
        ordering = ['-count']
        verbose_name_plural = "Popular Searches"


class UserInterest(models.Model):
    i_category = models.ManyToManyField('hubur_apis.Category')
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.i_user.get_name()}"

    class Meta:
        db_table = 'user_interest_db'
        ordering = ['-created_at']
        verbose_name_plural = "User Interest"


class TrendingDiscount(models.Model):
    name = models.CharField(max_length=255, unique=True)
    name_ar = models.CharField(max_length=255, unique=True, null=True)
    image = models.ImageField(upload_to="category_images/")
    i_business = models.ManyToManyField('hubur_apis.Business', related_name='trending_discount_business')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} | {self.is_active}"
    
    def get_edit_url(self):
        return reverse_lazy("edit_trending_discounts", kwargs={"discount_id": self.id})
    
    def get_delete_url(self):
        return reverse_lazy("delete_trending_discounts", kwargs={"pk": self.id})

    class Meta:
        db_table = 'trending_discount_db'
        ordering = ['-created_at']
        verbose_name_plural = "Trending Discount"



class Voting(models.Model):
    vote = models.BooleanField()
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vote} | {self.i_user.get_name()} | {self.i_business.name}"
    
    class Meta:
        db_table = 'voting_db'
        ordering = ['-created_at']
        verbose_name_plural = "Voting"


class MyFavourite(models.Model):
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE, null=True, blank=True)
    i_content = models.ForeignKey('hubur_apis.Content', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.i_user.get_name()} | {self.i_business.name}"
    
    class Meta:
        db_table = 'my_fav_db'
        ordering = ['-created_at']
        verbose_name_plural = "My Favourite"


class Visited(models.Model):
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.i_user.get_name()} | {self.i_business.name}"
    
    class Meta:
        db_table = 'my_visited'
        ordering = ['-created_at']
        verbose_name_plural = "My Visited"


class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = "FAQs"
        ordering = ['-created_at']


class Other(models.Model):
    about_us = models.TextField(blank=True, null=True)
    terms_condition = models.TextField(blank=True, null=True)
    privacy_policy = models.TextField(blank=True, null=True)
    disclaimer = models.TextField(blank=True, null=True)
    about_us_ar = models.TextField(blank=True, null=True)
    terms_condition_ar = models.TextField(blank=True, null=True)
    privacy_policy_ar = models.TextField(blank=True, null=True)
    disclaimer_ar = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.updated_at.date()} | {self.updated_at.time()}"

    class Meta:
        verbose_name_plural = "Terms, privacy Policy etc.."


class ContactUs(models.Model):
    country_code = models.CharField(max_length=5)
    mobile = models.CharField(max_length=15, unique=True)
    uan = models.CharField(max_length=15, unique=True)
    whatsapp = models.CharField(max_length=15, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.updated_at.date()} | {self.updated_at.time()}"

    class Meta:
        verbose_name_plural = "Contact Details"


class Booking(models.Model):
    STATUS_CHOICE = (
        (1, "Pending"),
        (2, "Accepted"),
        (3, "Cancelled"),
        (4, "Expired")
    )
    booking_no = models.CharField(max_length=50)
    persons = models.IntegerField(default=0)
    date = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_CHOICE, default=1) 
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)
    reason = models.CharField(max_length=100, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"{self.i_user.get_name()} | {self.i_business.name} | {self.date.date()} | {self.date.time()}"

    def get_booking_accept_url(self):
        return reverse_lazy("accept_booking", kwargs={"book_id": self.pk})
    
    def get_booking_cancel_url(self):
        return reverse_lazy("cancel_booking", kwargs={"book_id": self.pk})

    class Meta:
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']


class MyBookmark(models.Model):
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.i_user.get_name()} | {self.i_business.name}"
    
    class Meta:
        db_table = 'my_bookmark_db'
        ordering = ['-created_at']
        verbose_name_plural = "My Bookmark"


class Offers(models.Model):
    TYPE_CHOICE = (
        (1, "Daily"),
        (2, "Weekly"),
        (3, "Monthly"),
        (4, "Hot")
    )
    DISCOUNT_CHOICE = (
        (1, "Percentage"),
        (2, "Fixed")
    )
    name = models.CharField(max_length=1000)
    name_ar = models.CharField(max_length=1000, null=True)
    type = models.IntegerField(choices=TYPE_CHOICE, default=1)
    image = models.ImageField(upload_to="offer_images/", null=True, blank=True)
    discount_price = models.IntegerField()
    discount_type = models.IntegerField(choices=DISCOUNT_CHOICE, default=1)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    is_expiry = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)
    i_content = models.ManyToManyField('hubur_apis.Content')
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} | {self.get_type_display()} | {self.i_business.name} | {self.is_active}"
    
    def get_edit_url(self):
        return reverse_lazy("edit_offer", kwargs={"offer_id": self.id})
    
    def get_delete_url(self):
        return reverse_lazy("delete_offer", kwargs={"pk": self.id})
    
    class Meta:
        db_table = 'offer_db'
        ordering = ['-created_at']
        verbose_name_plural = "Offers"


class Attributes(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        db_table = 'attributes_db'
        ordering = ['-created_at']
        verbose_name_plural = "Attributes"


class SavedOffers(models.Model):
    i_content = models.ForeignKey('hubur_apis.Content', on_delete=models.CASCADE)
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.i_user.get_name()} | {self.i_business.name}"
    
    class Meta:
        db_table = 'saved_offer_db'
        ordering = ['-created_at']
        verbose_name_plural = "Saved Offers"


class Reviews(models.Model):
    display_name = models.CharField(max_length=225, null=True, blank=True)
    display_image = models.CharField(max_length=225, null=True, blank=True)
    review = models.CharField(max_length=5000)
    i_content = models.ForeignKey('hubur_apis.Content', on_delete=models.CASCADE, null=True, blank=True)
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE, null=True, blank=True)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE, null=True, blank=True)
    rate = models.FloatField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.i_user:
            return f"rating {self.rate} star(s) | {self.i_user.get_name()} | {self.i_content.name}"
        else:
            return f"rating {self.rate} star(s) | {self.display_name}"
    
    class Meta:
        db_table = 'review_db'
        ordering = ['-created_at']
        verbose_name_plural = "Reviews"


class Notification(models.Model):
    TYPE_CHOICE = (
        (1, "Redeem"),
        (2, "Follow/Unfollow"),
        (3, "Message"),
        (4, "Friend Story"),
        (5, "Saved Item Expiry Day"),
        (6, "Vendor Created Deal"),
        (7, "Avail Offer"),
        (8, "Review"),
    )
    user = models.ForeignKey('hubur_apis.UserProfile', related_name='receiver', on_delete=models.CASCADE)
    sender = models.ForeignKey('hubur_apis.UserProfile', related_name='sender', on_delete=models.CASCADE)
    content = models.ForeignKey('hubur_apis.Content', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=512, null=False, blank=False)
    title_ar = models.CharField(max_length=512, null=True)
    notification_type = models.IntegerField(choices=TYPE_CHOICE, null=True, blank=True)
    code = models.CharField(max_length=12, null=True, blank=True)
    body = models.CharField(max_length=512, null=False, blank=False)
    body_ar = models.CharField(max_length=512, null=True)
    reviewed = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    action = models.CharField(max_length=512, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} | {self.get_notification_type_display()} | {self.user.get_name()}"
    
    class Meta:
        db_table = 'notification_db'
        ordering = ['-created_at']
        verbose_name_plural = "Notifications"


class FriendList(models.Model):
    i_user = models.ForeignKey('hubur_apis.UserProfile', related_name='user', on_delete=models.CASCADE)
    friends = models.ForeignKey('hubur_apis.UserProfile', related_name='friends', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return f"{self.i_user.get_name()} | {self.friends.get_name()}"

    
    class Meta:
        db_table = 'friend_list_db'
        ordering = ['-created_at']
        verbose_name_plural = "Friend List"



class RewardPoints(models.Model):
    TYPE_CHOICE = (
        (1, "Check-In"),
        (2, "Redemption"),
        (3, "Story"),
        (4, "Vote"),
    )
    type = models.PositiveIntegerField(choices=TYPE_CHOICE, default=1)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.get_type_display()} | {self.points}"
    
    class Meta:
        db_table = 'reward_points_db'
        verbose_name_plural = "Reward Points"


class Level(models.Model):
    TYPE_CHOICE = (
        (1,"Gold"),
        (2,"Silver"),
        (3,"Bronze")
    )
    name = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    description_ar = models.CharField(max_length=255, null=True, blank=True)
    type = models.PositiveIntegerField(choices=TYPE_CHOICE,default=3)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} | {self.get_type_display()} | {self.points}"
    
    class Meta:
        db_table = 'level_db'
        verbose_name_plural = "Levels"


class UserReward(models.Model):
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    i_business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE)
    i_content = models.ForeignKey('hubur_apis.Content', on_delete=models.CASCADE, null=True, blank=True)
    i_point = models.ForeignKey('hubur_apis.RewardPoints', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def total_points(self):
        total = sum(UserReward.objects.filter(i_user=self.i_user).values_list('i_point__points',flat=True))
        return total
    
    @property
    def user_level(self):
        user_points = int(self.total_points)
        all_levels = Level.objects.all()
        gold = all_levels.filter(type=1).first()
        silver = all_levels.filter(type=2).first()
        bronze = all_levels.filter(type=3).first()

        if gold and silver and bronze:
            if user_points >= gold.points:
                obj = {"name":gold.name, "name_ar":gold.name_ar, "obj":gold}

            elif user_points >= silver.points:
                obj = {"name":silver.name, "name_ar":silver.name_ar, "obj":silver}

            elif user_points >= bronze.points:
                obj = {"name":bronze.name, "name_ar":bronze.name_ar, "obj":bronze}

            else:
                obj = {"name":"Level 0", "name_ar":"المستوى 0", "obj":None}
            
            return obj

    def __str__(self):
        if self.i_content:
            return f"{self.i_user.get_name()} | {self.i_content.name} | {self.i_point.get_type_display()} | {self.i_point.points} || Total points are: {self.total_points} | {self.user_level['name']}"
        else:
            return f"{self.i_user.get_name()} | {self.i_business.name} | {self.i_point.get_type_display()} | {self.i_point.points} || Total points are: {self.total_points} | {self.user_level['name']}"
    
    class Meta:
        db_table = 'user_reward_db'
        ordering = ['-created_at']
        verbose_name_plural = "User Reward"


class Message(models.Model):
    type_choice = (
        (1, "text"),
        (2, "image"),
        (3, "audio"),
        (4, "video"),
        (5, "profile"),
        (6, "story"),
        (7, "business"),
        (8, "content")
    )
    type = models.IntegerField(choices=type_choice, default=1)
    sender = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE, related_name='msg_sender')
    receiver = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE, related_name='msg_receiver')
    channel_id = models.CharField(max_length=100)
    content = models.CharField(max_length=500, null=True, blank=True)
    share_data = models.JSONField(null=True, blank=True)
    attachment = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.content:
            return f'{self.sender.get_name()} | {self.receiver.get_name()} | {self.channel_id} | {self.content} | {self.get_type_display()}'
        elif self.share_data:
            return f'{self.sender.get_name()} | {self.receiver.get_name()} | {self.channel_id} | {self.share_data} | {self.get_type_display()}'
        else:
            return f'{self.sender.get_name()} | {self.receiver.get_name()} | {self.channel_id} | {self.attachment} | {self.get_type_display()}'
    
    class Meta:
        db_table = 'message_db'
        ordering = ['-created_at']
        verbose_name_plural = "Messages"

    
class Chat(models.Model):
    user_1 = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE, related_name='user_1')
    user_2 = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE, related_name='user_2')
    channel_id = models.CharField(max_length=100, unique=True)
    last_message = models.CharField(max_length=500, default="")
    is_read = models.BooleanField(default=False)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_1.get_name()} | {self.user_2.get_name()} | {self.channel_id} | {self.last_message}'
    
    class Meta:
        db_table = 'chat_db'
        ordering = ['-updated_at']
        verbose_name_plural = "Chats"


class UserOnlineStatus(models.Model):
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.i_user.get_name()} | {self.is_online}'
    
    class Meta:
        db_table = 'user_online_status_db'
        ordering = ['-created_at']
        verbose_name_plural = "User Online Status"

class AppleToken(models.Model):
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    token = models.CharField(max_length=250, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.i_user.get_name()} | {self.token}'
    
    class Meta:
        db_table = 'apple_token_db'
        ordering = ['-created_at']
        verbose_name_plural = "Apple Token"

class NotificationSettings(models.Model):
    i_user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    update_on_whatsapp = models.BooleanField(default=True)
    promotional_messages = models.BooleanField(default=True)
    promotional_email = models.BooleanField(default=True)
    all_notifications = models.BooleanField(default=True)
    new_offer = models.BooleanField(default=True)
    offer_expire = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.i_user.get_name()}'
    
    class Meta:
        db_table = 'notification_settings_db'
        ordering = ['-created_at']
        verbose_name_plural = "Notification Settings"


class Subscription(models.Model):
    SUBSCRIPTION_TYPE_CHOICES = (
        (1, 'Free'),
        (2, 'Monthly'),
        (3, 'Yearly'),
    )
    SUBSCRIPTION_TYPE_CHOICES_AR = (
        (1, 'حر'),
        (2, 'شهريا'),
        (3, 'سنوي'),
    )
    name = models.CharField(max_length=100)
    name_ar = models.CharField(max_length=100, null=True)
    description = models.TextField()
    description_ar = models.TextField(null=True)
    duration_months = models.PositiveIntegerField(max_length=2, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_type = models.IntegerField(choices=SUBSCRIPTION_TYPE_CHOICES, default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_edit_url(self):
        return reverse_lazy("edit_subscription", kwargs={"sub_id": self.id})
    
    def get_delete_url(self):
        return reverse_lazy("delete_subscription", kwargs={"pk": self.id})
    
    def get_add_feature_url(self):
        return reverse_lazy("create_subscription_feature", kwargs={"sub_id": self.id})

    def get_view_feature_url(self):
        return reverse_lazy("list_subscriptions_feature", kwargs={"sub_id": self.id})
    
    class Meta:
        db_table = 'subscription_db'
        ordering = ['-created_at']
        verbose_name_plural = "Subscriptions"


class SubscriptionFeature(models.Model):
    feature_name = models.CharField(max_length=100)
    feature_name_ar = models.CharField(max_length=100, null=True)
    subscription = models.ForeignKey('hubur_apis.Subscription', on_delete=models.CASCADE, related_name='features')
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.feature_name
    
    def get_edit_url(self):
        return reverse_lazy("edit_subscription_feature", kwargs={"sub_id": self.subscription.id, "feature_id": self.id})
    
    def get_delete_url(self):
        return reverse_lazy("delete_subscription_feature", kwargs={"pk": self.id})
    
    class Meta:
        db_table = 'subscription_feature_db'
        ordering = ['-created_at']
        verbose_name_plural = "Subscription Features"


class UserSubscription(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    subscription = models.ForeignKey('hubur_apis.Subscription', on_delete=models.CASCADE, related_name='user_subscription')
    user = models.ForeignKey('hubur_apis.UserProfile', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subscription.name} | {self.user.first_name} | {self.user.last_name}"
    
    class Meta:
        db_table = 'user_subscription_db'
        ordering = ['-created_at']
        verbose_name_plural = "User Subscription"


class Tags(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    business = models.ForeignKey('hubur_apis.Business', on_delete=models.CASCADE, null=True, blank=True)
    content = models.ForeignKey('hubur_apis.Content', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'tags_db'
        ordering = ['-created_at']
        verbose_name_plural = "Tags"


class Campaign(models.Model):
    title = models.CharField(max_length=30)
    title_ar = models.CharField(max_length=30, null=True)
    desc = models.TextField(max_length=100)
    desc_ar = models.TextField(max_length=100, null=True)
    i_business = models.OneToOneField('hubur_apis.Business', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} | {self.i_business.name}"
    
    def get_edit_url(self):
        return reverse_lazy("edit_promotion", kwargs={"promo_id": self.id})
    
    def get_delete_url(self):
        return reverse_lazy("delete_promotion", kwargs={"pk": self.id})


    class Meta:
        db_table = 'campaign_db'
        ordering = ['-created_at']
        verbose_name_plural = "Campaign"