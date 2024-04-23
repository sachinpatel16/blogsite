from django.urls import path,include
from blog import views

from django.conf.urls.static import static
from mysite import settings


from django.conf.urls import handler404
handler404 = 'blog.views.custom_404'

urlpatterns = [
    path("",include('blog.urls')),
    path("login/",views.user_login,name='login'),
    path("logout/",views.user_logout,name='logout'),
    path("registration/",views.user_registration,name='reg'),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
