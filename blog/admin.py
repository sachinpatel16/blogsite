from django.contrib import admin
# from django.contrib.auth.models import User
from blog.models import User
from blog.models import Post,Coment,Like,Dislike,Multimedia,Category,Profile


admin.site.register(Coment)
admin.site.register(Post)
admin.site.register(Profile)
# admin.site.register(UserData)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(Multimedia)
admin.site.register(Category)