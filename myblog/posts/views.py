from django.shortcuts import render, redirect, get_object_or_404

from .models import Post
from .forms import PostForm



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
