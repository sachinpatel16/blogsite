from django.db.models.query import QuerySet
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.utils import timezone
from blog.models import Post,Coment,Category,Multimedia,Profile
from django.contrib.auth.models import User
from blog.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout

from django.http import Http404

# from blog.forms import PostForm,CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin # class based view
from django.contrib.auth.decorators import login_required  # function based view
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.
# def index(request):
#     return render(request,'blog/index.html')

    # return HttpResponse("Page not found")


class IndexListView(ListView):
    context_object_name = 'post_list'
    model = Post
    ordering = ['-id']
    
    def get_context_data(self, **kwargs):
        contex =  super().get_context_data(**kwargs)
        contex['user_data'] = Profile.objects.all()
        return contex

class PostDetailView(DetailView):
    context_object_name = 'post_detail'
    model = Post 
    
    def get_object(self, queryset=None):
        try:
            # Attempt to retrieve the post object as usual
            return super().get_object(queryset)
        except:
            # Handle the case when no post is found matching the query
            return redirect('/404/')
        
    def post(self,request, *args,**kwargs):
        if request.method == 'POST':
            post = self.get_object()
            # name = request.POST.get('name')
            text = request.POST.get('text')
            
            coment = Coment.objects.create(post=post,commenter=request.user,text=text)
            return redirect('post_detail', pk=post.pk)
    
    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['user_prof'] = Profile.objects.all()
        contex['user_category'] = Category.objects.all()
        return contex
    # def get_context_data(self, **kwargs):
    #     contex = super().get_context_data(**kwargs)
    #     contex['user_coment'] = Coment.objects.all()
    #     return contex

@login_required
def postlist(request):
    use = request.user.id
    post_list = Post.objects.filter(auther = use).order_by('-put_date')
    data = {
        'post_list':post_list
    }
    return render(request,'blog/post.html',context=data)


@login_required
def postUpdate(request,pk):
    detail = get_object_or_404(Post, id=pk)
    print("titel:",detail.title)
    media = Multimedia.objects.get(id = pk)
    category = Category.objects.all()
    user = User.objects.all()
    
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        author_name  = request.POST['author']
        categorye = request.POST['category']
        pic = request.FILES.get('post_pic')
                
        author = User.objects.get(username=author_name)
        # post_data = Post.objects.create(title=title,content=content,auther=author)
        detail.title = title
        detail.content = content
        detail.auther = author
        detail.categories.add(Category.objects.get(name = categorye))
        detail.save()
        # post_data.categories.add(Category.objects.get(name=categorye))
        media.post = detail 
        media.file = pic
        media.save()
        return redirect('postlist')
    data ={
        'category':category,
        'detail':detail,
        'media':media
    }
    return render(request,'blog/updatePost.html',context=data)

def about(request):
    return render(request,'blog/about.html')
# def post(request):
#     return render(request,'blog/post.html')

@login_required
def profile(request):
    user = request.user.id
    print("user:",user)
    if request.method == 'POST':
        user_pic = request.FILES.get('post_pic')
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        
        username = User.objects.get(username=name)
        
        try:
            if Profile.objects.get(name_id = user):
                u = Profile.objects.get(name_id = user)
                u.name=username
                u.user_pic=user_pic
                u.bio=bio
                u.save()
            return redirect('/')
        except:
            prof = Profile.objects.create(name=username,user_pic=user_pic,bio=bio)
            return redirect('/')
    else:
        pass
    return render(request,'blog/profile.html')


@login_required
def deletePost(request,pk):
    data = get_object_or_404(Post,id=pk)
    data.delete()
    return redirect('postlist')

@login_required
def post(request):
    category = Category.objects.all()
    user = User.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        author_name  = request.POST['author']
        categorye = request.POST['category']
        pic = request.FILES.get('post_pic')
                
        author = User.objects.get(username=author_name)
        post_data = Post.objects.create(title=title,content=content,auther=author)
        post_data.categories.add(Category.objects.get(name=categorye))
        Multimedia.objects.create(post=post_data, file=pic)
        return redirect('index')
    data ={
        'category':category
    }
    return render(request,'blog/singlepost.html',context=data)

def contact(request):
    return render(request,'blog/contact.html')



#########################################
def user_login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username,password=password)
        
        if user:
            
            if user.is_active:
                login(request,user)
                return redirect('/')
            else:
                return HttpResponse("Account is not found")
        else:
            print("Some trie to login failed")
            print(f'username {username} and password {password}')
            return HttpResponse("Invalid detail suplied")
    return render(request,'blog/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

def user_registration(request):
    registration = False
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            form.save()
            registration = True
            
            return redirect('/')
        else:
            print(form.errors)
    else:
        form = UserCreationForm()

    data ={
        'form':form,
        'registration':registration
    }
    return render(request,'blog/registration.html',context=data)

############################################

def custom_404(request):
    # return render(request, 'blog/404.html', status=404)
    return HttpResponse("404 not found")