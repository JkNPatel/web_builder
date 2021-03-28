from django.urls import path,re_path
from . import views
app_name = 'website'

urlpatterns = [
    re_path(r'^(?P<website>[\w-]+)/(?P<page>[\w-]+)/$', views.MasterView.as_view() , name="web_preview"),
    re_path(r'^(?P<website>[\w-]+)/$', views.MasterView.as_view() , name="preview"),
    path('login', views.UserLogin.as_view() , name="login"),
    path('logout', views.UserLogout.as_view() , name="logout"),
    path('register', views.UserRegister.as_view() , name="register"),
    path('dashboard', views.UserDashboard.as_view() , name="dashboard"),
    path('add-website', views.AddWebsite.as_view() , name="add_website"),
    path('add-page', views.AddPage.as_view() , name="add_page"),
    path('add-element', views.AddElement.as_view() , name="add-element"),
    path('remove-element', views.RemoveElement.as_view() , name="remove-element"),
    path('updown-element', views.UpDownElement.as_view() , name="updown-element"),
    path('edit', views.EditElement.as_view() , name="edit-element"),
    re_path(r'^edit/(?P<website>[\w-]+)/(?P<page>[\w-]+)/$', views.MasterEdit.as_view() , name="web_editor"),
    re_path(r'^edit/(?P<website>[\w-]+)/$', views.MasterEdit.as_view() , name="editor"),
    path('sub_users', views.All_sub_user.as_view() , name="sub_users"),
    path('subuser-access', views.Sub_user_access.as_view() , name="subuser_access"),
    path('editMeta', views.EditMeta.as_view() , name="edit_meta"),
    path('editHeader', views.EditHeader.as_view() , name="edit_header"),
    
]

