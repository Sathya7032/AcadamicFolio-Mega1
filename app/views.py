from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def register_view(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			######################### mail system ####################################
			htmly = get_template('email.html')
			d = { 'username': username }
			subject, from_email, to = 'welcome', 'your_email@gmail.com', email
			html_content = htmly.render(d)
			msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()
			##################################################################
			messages.success(request, f'Your account has been created ! You are now able to log in')
			return redirect('login')
	else:
		form = UserRegisterForm()
		messages.warning(request, f'something went wrong, please try again..')
	return render(request, 'register.html', {'form': form, 'title':'register here'})

################ login forms###################################################

def login_view(request):
	if request.method == 'POST':
		# AuthenticationForm_can_also_be_used__
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email = email, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {email} !!')
			return redirect('homepage')
		else:
			messages.info(request, f'username or password is incorrect')
	form = AuthenticationForm()
	return render(request, 'signin.html', {'form':form, 'title':'log in'})


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


def index(request):
    return render(request,"index.html")


@login_required
def code(request):
    return render(request,"user/code.html")

def contact(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject2 = request.POST.get('subject')
        message1 = request.POST.get('message')
        print(name)
        query = Contact(name=name,email=email,subject=subject2,message=message1)
        query.save()

        subject = 'THANK YOU FOR CONTACTING ME '
        message = f'Hi {name}, Thank you so much for reaching out to me. we will get back to you soon.. '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail( subject, message, email_from, recipient_list )

        
        subject1 = 'HELLOW SIR SOMEONE CONTACTED YOU'
        message = f'Hi k satyanarayana chary,  Some one contacted you details are:- \n username - {name},\n  email - {email},\n subject - {subject2},\n message - {message1} \n'
        email_from = settings.EMAIL_HOST_USER
        recipient_list1 = ['acadamicfolio@gmail.com', ]
        send_mail( subject1, message, email_from, recipient_list1 )

        messages.success(request,"Thanks for contacting us ,we will contact you soon..")
        return redirect('/contact/')
    return render(request,"contact.html")

@login_required
def homepage(request):
     user = request.user
     tasks=Task.objects.filter(user=user)
     active_tasks = tasks.filter(completed=False).count()
     completed_tasks = tasks.filter(completed=True).count()
     total_tasks = tasks.count()
     your_blogs = Blogs.objects.filter(user=user)
     your_memes = Meme.objects.filter(user=user)

     context = {
        'active_tasks': active_tasks,
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
        'your_blogs': your_blogs,
        'your_memes':your_memes
    }
     return render(request,"homepage.html",context)

@login_required
def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'user/todo.html', {'tasks': tasks})

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            new_todo=form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            messages.success(request, f'Your notes is added successfully !....')
            return redirect('/tasks/')
    else:
        form = TaskForm()
    return render(request, 'user/todo.html', {'form': form})

def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.completed = True
    task.save()
    return redirect('/tasks/')

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.delete()
    return redirect('/tasks/')


@login_required
def post_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.user = request.user
            new_blog.save()
            return redirect('/blog_detail/')  # Redirect to a view that lists all blogs
    else:
        form = BlogForm()
    return render(request, 'user/addBlog.html', {'form': form})	  


@login_required
def blogs(request):
      
      blog_list = Blogs.objects.all()
      
      paginator = Paginator(blog_list, 10)  # Show 10 blogs per page

      page_number = request.GET.get('page')
      try:
         blogs = paginator.page(page_number)
      except PageNotAnInteger:
        # If page is not an integer, deliver first page.
         blogs = paginator.page(1)
      except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
         blogs = paginator.page(paginator.num_pages)

      query = request.GET.get('q','')
      results = Blogs.objects.filter(title__icontains=query)   

      return render(request,"user/blogs.html",{'blogs':blogs,'results':results,'query':query})


@login_required
def singleBlog(request, blog_id):
      blog = get_object_or_404(Blogs, pk=blog_id)
      if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            comment.save()
            
      else:
            form = CommentForm()
      
      return render(request,"user/singleBlog.html",{'blog':blog})


@login_required
def tutorials(request):
     tutorials = TutorialName.objects.all()
     return render(request,"user/tutorials.html",{'tutorials':tutorials})


@login_required
def tutorialView(request,tut_id):
    tutorialName_id = get_object_or_404(TutorialName, pk=tut_id)
    posts = TutorialPost.objects.filter(tutorialName_id=tutorialName_id)
    return render(request,"user/tutorialView.html",{'tutorialName_id':tutorialName_id,'posts':posts})


@login_required
def tutorialPost(request,post_id):
     post = get_object_or_404(TutorialPost,pk=post_id)
     return render(request,"user/post.html",{'post':post})

@login_required
def meme(request):
     meme = Meme.objects.all()
     query = request.GET.get('q','')
     results = Meme.objects.filter(description__icontains=query)
     return render(request,"user/meme.html",{'meme':meme,'results': results, 'query': query})


@login_required
def upload_meme(request):
    if request.method == 'POST':
        form = MemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme=form.save(commit=False)
            meme.user = request.user
            meme.save()
            return redirect('/meme/')
    else:
        form = MemeForm()
    return render(request, 'user/upload_meme.html', {'form': form})