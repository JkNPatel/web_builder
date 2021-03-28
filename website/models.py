from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .manager import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Website(models.Model):
    website_user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    website_name = models.CharField(max_length=200)
    website_logo1 = models.ImageField()
    website_logo2 = models.ImageField()
    website_favicon = models.ImageField()
    website_url = models.URLField()
    website_is_rtl = models.BooleanField(default=0)

    # foreign key of language table
    website_language = models.IntegerField(default=0)

    website_is_search =  models.BooleanField(default=0)
    website_is_active =  models.BooleanField(default=1)
    website_created_date = models.DateTimeField(default=timezone.now)
    website_updated_date = models.DateTimeField(default=timezone.now)

    # foreign key of page table
    website_homepage_id = models.IntegerField(default=0)
    
    # foreign key of Template table
    website_template_id = models.IntegerField(default=0)

    website_visitor_count = models.IntegerField(default=0)

    # foreign key of font family table
    website_primary_font_id = models.IntegerField(default=0)
    website_secondary_font_id = models.IntegerField(default=0)

     # foreign key of font style id table
    website_primary_font_style_id = models.IntegerField(default=0)
    website_secondary_font_style_id = models.IntegerField(default=0)


class Page(models.Model):
    page_website_id = models.ForeignKey(Website, on_delete=models.CASCADE)
    page_name = models.CharField(max_length=200)
    page_url = models.TextField(default=None)
    page_title = models.CharField(max_length=200)
    page_desc = models.TextField()
    page_author = models.CharField(max_length=200)
    page_is_active =  models.BooleanField(default=1)
    page_created_date = models.DateTimeField(default=timezone.now)
    page_updated_date = models.DateTimeField(default=timezone.now)

    # foreign key of page style table
    page_style_id = models.IntegerField(default=0)

    page_name = models.CharField(max_length=200)
    page_is_container =  models.BooleanField(default=1)

    def __str__(self):
        return str(self.id)
    
class SubUser(models.Model):
    sub_user_uname = models.CharField(max_length=200)
    sub_user_pass = models.CharField(max_length=200)
    sub_user_last_login = models.DateTimeField(default=timezone.now)
    sub_user_is_active =  models.BooleanField(default=1)
    sub_user_created_date = models.DateTimeField(default=timezone.now)
    sub_user_owner_id = models.IntegerField(default=0)
    
   
class SubUserAccess(models.Model):
    sub_access_website_id = models.ForeignKey(Website, on_delete=models.CASCADE)
    sub_access_user_id = models.ForeignKey(SubUser, on_delete=models.CASCADE)
    sub_access_is_active =  models.BooleanField(default=1)
    sub_access_created_date = models.DateTimeField(default=timezone.now)
    sub_access_owner_id = models.IntegerField(default=0)

class Meta(models.Model):
    meta_in_head_content = models.TextField()
    meta_begin_body_content = models.TextField()
    meta_end_body_content = models.TextField()
    meta_is_active =  models.BooleanField(default=1)
    meta_created_date = models.DateTimeField(default=timezone.now)
    meta_updated_date = models.DateTimeField(default=timezone.now)
    # foreign key of website table
    meta_website_id = models.ForeignKey(Website, on_delete=models.CASCADE)
"""
class FontFamily(models.Model):
    font_family_name = models.CharField(max_length=200)
    font_family_type = models.CharField(max_length=200)
    font_family_is_active = models.BooleanField(default=1)
    font_family_created_date = models.DateTimeField(default=timezone.now)
    font_family_updated_date = models.DateTimeField(default=timezone.now)

class FontStyle(models.Model):
    font_weight = models.CharField(max_length=200)
    font_style = models.CharField(max_length=200)
    font_size = models.CharField(max_length=200)
    font_is_active = models.BooleanField(default=1)
    font_created_date = models.DateTimeField(default=timezone.now)
    font_updated_date = models.DateTimeField(default=timezone.now)
"""

class PageElement(models.Model):    #Element container
    page_element_page_id = models.ForeignKey(Page, on_delete=models.CASCADE)
    page_element_table = models.CharField(max_length=200)
    page_element_table_id = models.IntegerField()
    page_element_order = models.IntegerField()
    page_element_is_active = models.BooleanField(default=1)
    page_element_file = models.CharField(max_length=200)
    page_element_created_date = models.DateTimeField(default=timezone.now)
    page_element_updated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

class Header(models.Model):
    header_website_id = models.ForeignKey(Website, on_delete=models.CASCADE)
    header_contact = models.CharField(max_length=200)
    header_email = models.CharField(max_length=200)
    header_facebook = models.CharField(max_length=200)
    header_twitter = models.CharField(max_length=200)
    header_instagram = models.CharField(max_length=200)
    header_tagline = models.CharField(max_length=200)
    header_file = models.CharField(max_length=200)
    header_is_active = models.BooleanField(default=1)
    header_created_date = models.DateTimeField(default=timezone.now)
    header_updated_date = models.DateTimeField(default=timezone.now)

class Menu1(models.Model):
    menu1_header_id = models.ForeignKey(Header, on_delete=models.CASCADE)
    menu1_title = models.CharField(max_length=200)
    menu1_order = models.IntegerField()
    menu1_link_type = models.CharField(max_length=200)
    menu1_link_url = models.TextField()
    menu1_is_active = models.BooleanField(default=1)
    menu1_created_date = models.DateTimeField(default=timezone.now)
    menu1_updated_date = models.DateTimeField(default=timezone.now)

class Menu2(models.Model):
    menu2_menu1_id = models.ForeignKey(Menu1, on_delete=models.CASCADE)
    menu2_title = models.CharField(max_length=200)
    menu2_order = models.IntegerField()
    menu2_link_type = models.CharField(max_length=200)
    menu2_link_url = models.TextField()
    menu2_is_active = models.BooleanField(default=1)
    menu2_created_date = models.DateTimeField(default=timezone.now)
    menu2_updated_date = models.DateTimeField(default=timezone.now)

class Counter(models.Model):
    counter_title = models.CharField(max_length=200)
    counter_desc = models.TextField()
    counter_number = models.CharField(max_length=200)

    counter_icon1 = models.TextField()
    counter_text1 = models.CharField(max_length=200)
    counter_count1_prepend = models.CharField(max_length=200,default=None)
    counter_count1 = models.CharField(max_length=200)
    counter_count1_append = models.CharField(max_length=200,default=None)

    counter_icon2 = models.TextField()
    counter_text2 = models.CharField(max_length=200)
    counter_count2_prepend = models.CharField(max_length=200,default=None)
    counter_count2 = models.CharField(max_length=200)
    counter_count2_append = models.CharField(max_length=200,default=None)

    counter_icon3 = models.TextField()
    counter_text3 = models.CharField(max_length=200)
    counter_count3_prepend = models.CharField(max_length=200,default=None)
    counter_count3 = models.CharField(max_length=200)
    counter_count3_append = models.CharField(max_length=200,default=None)

    counter_icon4 = models.TextField()
    counter_text4 = models.CharField(max_length=200)
    counter_count4_prepend = models.CharField(max_length=200,default=None)
    counter_count4 = models.CharField(max_length=200)
    counter_count4_append = models.CharField(max_length=200,default=None)


    counter_is_active = models.BooleanField(default=1)

    counter_bg_image = models.ImageField()
    counter_bg_color = models.CharField(max_length=200)
    counter_icon_color = models.CharField(max_length=200)
    counter_title_color = models.CharField(max_length=200)
    counter_text_color = models.CharField(max_length=200)
    counter_animation_type = models.CharField(max_length=200,default=None)
    counter_animation_delay = models.CharField(max_length=200,default=None)

    counter_status = models.CharField(max_length=200)
    counter_created_date = models.DateTimeField(default=timezone.now)
    counter_updated_date = models.DateTimeField(default=timezone.now)
    

    def _str_(self):
        return str(self.id)
"""
class ReviewStyle(models.Model):
    review_style_class = models.CharField(max_length=200)
    review_style_is_active = models.BooleanField(default=1)
    review_style_created_date = models.DateTimeField(default=timezone.now)
    review_style_updated_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

class ReviewData(models.Model):
    review_data_style_id = models.IntegerField(default=0)
    review_data_element_id = models.ForeignKey(PageElement, on_delete=models.CASCADE)
    review_data_comment = models.TextField()
    review_data_image = models.ImageField()
    review_data_person_name = models.CharField(max_length=200)
    review_data_person_tag = models.CharField(max_length=200) 
    review_data_is_active = models.BooleanField(default=1)
    review_data_created_date = models.DateTimeField(default=timezone.now)
    review_updated_date = models.DateTimeField(default=timezone.now)
    review_data_title = models.CharField(max_length=200)
    review_data_subtitle = models.CharField(max_length=200)
    review_data_desc = models.TextField()
    review_data_bg_color = models.CharField(max_length=200)
    review_data_color = models.CharField(max_length=200)
    review_data_top_margin =  models.IntegerField(default=0)
    review_data_top_padding =  models.IntegerField(default=0)
    review_data_bottom_margin =  models.IntegerField(default=0)
    review_data_bottom_padding =  models.IntegerField(default=0)

    # foreign key of font family table
    review_data_primary_font_id = models.IntegerField(default=0)
    review_data_secondary_font_id = models.IntegerField(default=0)

    # foreign key of font style id table
    review_data_primary_font_style_id = models.IntegerField(default=0)
    review_data_secondary_font_style_id = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)

    """