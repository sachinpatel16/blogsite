
from django.urls import path
from blog import views
from django.contrib import admin




# app_name = 'blog'
urlpatterns = [
    path("",views.IndexListView.as_view(),name='index'),
    path("admin/", admin.site.urls,name='admin'),
    path("postlist/",views.postlist,name='postlist'),
    path("postlist/<int:pk>/",views.postUpdate,name='updatepost'),
    path("del/<int:pk>/",views.deletePost,name='del'),
    path("profile/",views.profile,name='profile'),
    path("about/",views.about,name='about'),
    path("contact/",views.contact,name='contact'),
    path("post/",views.post,name='post'),
    path('404/', views.custom_404,name="404"),
    path("<slug:pk>",views.PostDetailView.as_view(),name='post_detail'),
]

