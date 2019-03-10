from django.shortcuts import render,HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

def post_index(request):
    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__contains=query)|
            Q(user__last_name__contains=query)
        ).distinct()

    paginator = Paginator(post_list, 5) # Show 25 contacts per page
    page = request.GET.get('sayfa')
    posts = paginator.get_page(page)

    return render(request, 'post/index.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'post' :post,
        'form': form,
    }
    return render(request, 'post/detail.html', context)


def post_create(request):
    if not request.user.is_authenticated:
        return Http404()

    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        messages.success(request, 'Başarılı Bir Şekilde Oluşturdunuz.')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form':form,
    }
    return render(request, 'post/form.html',context)


def post_update(request, slug):
    if not request.user.is_authenticated:
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None,request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save()
        messages.error(request, 'Başarılı Bir Şekilde Oluşturdunuz.', extra_tags='mesaj-basarili')
        return HttpResponseRedirect(post.get_absolute_url())

    context = {
        'form':form,
    }
    return render(request, 'post/form.html', context)


def post_delete(request, slug):
    if not request.user.is_authenticated:
        return Http404()

    post = get_object_or_404(Post, slug=slug)
    post.delete()

    return redirect("post:index")