from django.db.models.query import QuerySet
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.utils import timezone
from blog.models import Post,Coment,Category,Multimedia,Profile
from django.contrib.auth.models import User
from blog.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout

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
        return contex



def about(request):
    return render(request,'blog/about.html')
# def post(request):
#     return render(request,'blog/post.html')

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

def custom_404(request, exception):
    # return render(request, 'blog/404.html', status=404)
    return HttpResponse("404 not found")