import os
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from global_methods import file_size
from django.urls import reverse_lazy

# Create your models here.


class UserProfileManager(BaseUserManager):

    def create_user(self, username,first_name,last_name, email,country_code, gender, contact,terms_conditions=None , is_type = None,dob = None, address= None, password=None, profile_picture=None):

        if not any([ username,first_name,last_name,email]):
            raise ValueError(
                "[ name, last_name, email all fields are required")

        email = self.normalize_email(email=email)

        user = self.model(username=username,first_name=first_name,last_name=last_name, email=email, country_code=country_code, gender=gender, contact=contact,is_type=is_type, dob=dob, address=address, profile_picture=profile_picture, terms_conditions=terms_conditions)

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
    dob = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=225,null=True,blank=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", default='profile_pictures/logo_min.png', null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    terms_conditions = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def get_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f"{self.get_name()} | {self.email} | {self.country_code}-{self.contact}"

    def is_user(self):
        return self.role == 1

    def is_vendor(self):
        return self.role == 2
    
    def is_admin(self):
        return self.role == 3

    def is_superuser(self):
        return self.role == 4
    

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
    i_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
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


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
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
    image = models.ImageField(upload_to="category_images/", null=True,blank=True)
    i_category = models.ForeignKey(Category, on_delete=models.CASCADE)
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
    contact = models.CharField(max_length=15)
    country_code = models.CharField(max_length=5)
    address = models.CharField(max_length=255)
    long = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    logo_pic = models.ImageField(upload_to="business_images/", default='business_images/bag.png')
    i_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    i_subcategory = models.ManyToManyField(SubCategories)
    i_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    is_claimed = models.IntegerField(choices=IS_CLAIM_CHOICE, default=1)
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
        (3, "Restaurant"),	
        (4, "Health Care"),	
    )
    name = models.CharField(max_length=255)
    disc = models.CharField(max_length=255, null=True, blank=True)
    i_business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    picture = models.ImageField(upload_to="product_images/")
    content_type = models.IntegerField(choices=CONTENT_TYPE_CHOICE, default=1)
    i_sub_category = models.ManyToManyField(SubCategories)
    price = models.FloatField()
    i_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.i_sub_category.name} | {self.price} | {self.i_user.get_name()} | {self.is_active}"

    class Meta:
        db_table = 'contents'
        ordering = ['-created_at']
        verbose_name_plural = "Contents"
        unique_together = ('name', 'i_user',)

class ClaimBusiness(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    i_business = models.ForeignKey(Business, on_delete=models.CASCADE)
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
    )
    type = models.IntegerField(choices=TYPE_CHOICE)
    i_business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="other_images/")
    is_active = models.BooleanField(default=True)
    i_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.i_user.get_name()} | {self.is_active}"

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
    i_business = models.ForeignKey(Business, on_delete=models.CASCADE)
    i_day = models.ForeignKey(Day, on_delete=models.CASCADE)
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
    )	
    
    image = models.ImageField(upload_to="banner_images/", null=True, blank=True)	
    position = models.IntegerField(choices=POSITION_CHOICE)	
    i_subcatagory = models.ForeignKey(SubCategories, on_delete=models.CASCADE, null=True, blank=True)
    i_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
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
    image = models.ImageField(upload_to="brand_images/")
    founded_year = models.DateField()
    founded_country = models.CharField(max_length=255)
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
    i_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    updated_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="updated_user")
    i_business = models.ForeignKey(Business, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} | {self.i_user.get_name()} | {self.i_business.name} | {self.is_active}"

    class Meta:
        db_table = 'story_db'
        ordering = ['-created_at']
        verbose_name_plural = "Stories"


class Checkedin(models.Model):
    i_story = models.ForeignKey(Story, on_delete=models.CASCADE, null=True, blank=True)
    i_business = models.ForeignKey(Business, on_delete=models.CASCADE)
    other = models.CharField(max_length=255, null=True, blank=True)
    i_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
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
    i_content = models.ForeignKey(Content, on_delete=models.CASCADE)
    i_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
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
    name = models.CharField(max_length=255)
    url = models.URLField(max_length=255, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    catagory = models.CharField(max_length=20, null=True, blank=True)
    type_id = models.IntegerField()
    count = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} | {self.count} | {self.is_active}"

    class Meta:
        db_table = 'popular_search_db'
        ordering = ['-count']
        verbose_name_plural = "Popular Searches"


class UserInterest(models.Model):
    i_category = models.ManyToManyField(Category)
    i_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
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
    image = models.ImageField(upload_to="category_images/")
    i_business = models.ManyToManyField(Business, related_name='trending_discount_business')
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