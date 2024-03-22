from django.db.models.query import QuerySet
from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.utils import timezone
from blog.models import Post,Coment,Category,Multimedia
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

class IndexListView(ListView):
    context_object_name = 'post_list'
    model = Post
    ordering = ['-id']


class PostDetailView(DetailView):
    context_object_name = 'post_detail'
    model = Post 


def about(request):
    return render(request,'blog/about.html')
# def post(request):
#     return render(request,'blog/post.html')

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

