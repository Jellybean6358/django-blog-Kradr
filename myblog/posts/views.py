from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Post
from .forms import PostForm

def search_results(request):
    query=request.GET.get('q','')
    print(f"--- DEBUG: Received Query: '{query}' ---")
    results=[]
    if query:
        # Check if user is logged in as per your requirement
        if request.user.is_authenticated:
            results = Post.objects.filter(
                Q(title__icontains=query) | Q(text__icontains=query)
            )[:5]
            print(f"--- DEBUG: Found {results.count()} results ---")
    
    return render(request, 'posts/search_dropdown.html', {
        'results': results,
        'query': query
    })

def post_list(request):
    posts = Post.objects.all().order_by('-created_date')
    query = request.GET.get('q')

    if query and request.user.is_authenticated:
        # Complex search filter
        posts = posts.filter(Q(title__icontains=query) | Q(text__icontains=query))

    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request,pk):
    post=get_object_or_404(Post,pk=pk)
    return render(request,'posts/post_detail.html',{'post':post})

def post_delete(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=="POST":
        post.delete()
        return redirect('post_list')
    return render(request,'posts/post_confirm_delete.html',{'post':post})

def post_edit(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=="POST":
        form=PostForm(request.POST,instance=post)
        if form.is_valid():
            post=form.save()
            return redirect('post_list')
    else:
        form=PostForm(instance=post)
    return render(request, 'posts/post_edit.html',{'form':form,'post':post})

def post_new(request):
    if request.method=="POST":
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.save()
            return redirect('post_list')
    else: 
        form=PostForm()
    return render(request,'posts/post_edit.html',{'form':form})
        

def post_list(request):
    posts=Post.objects.all().order_by('-created_date')
    return render(request,'posts/post_list.html',{'posts':posts})

# Create your views here.
