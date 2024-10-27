import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import  HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt


from .models import User, NewPost, Like, Follow


def index(request):
    user = request.user
    if user.is_authenticated:
        posts = NewPost.objects.order_by("-post_date").all()
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        try:
            likes = Like.objects.filter(user=request.user).all()
            list_likes = []
            for like in likes:
                list_likes.append(like.post.pk)
                print(list_likes)
            return render(request, "network/index.html", {
                "posts": posts,
                'page_obj': page_obj,
                'likes': list_likes
            })
        except:
            pass
        return render(request, "network/index.html", {
            "posts": posts,
            'page_obj': page_obj
        })
    return HttpResponseRedirect(reverse("login"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required  
def new_post(request):
    if request.method == 'POST':
        user =  request.user
        author = User.objects.get(username=user)
        text = request.POST['text']
        post = NewPost.objects.create(author=author, text=text)
        post.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'network/new_post.html')

@csrf_exempt
def like_posts(request, id):
    post = get_object_or_404(NewPost, id= id)

    if request.method == 'POST':
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return JsonResponse({'total_likes': post.total_likes})
        like.save()
        return JsonResponse({'total_likes': post.total_likes})
    
        

def profile_page(request, user_profile):
    usern = get_object_or_404(User, username=user_profile)
    user_id=usern.id
    visitor= request.user
    posts = NewPost.objects.filter(author=user_id).all()
    posts = posts.order_by('-post_date').all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    follow = Follow.objects.filter(following=user_id).all()
    follows = Follow.objects.filter(user=usern).all()
    try:
        likes = Like.objects.filter(user=request.user).all()
        list_likes = []
        for like in likes:
            list_likes.append(like.post.pk)
            print(list_likes)
    except:
        pass
    if request.method == "POST":
        o = Follow.objects.all()
        try:
            of = o.get(user=visitor)
            of.set([usern])
            return HttpResponseRedirect(reverse('profile_page', args=[usern]))
        except:        
            os = o.create(user=visitor)
            os.following.set([usern])
            return HttpResponseRedirect(reverse('profile_page', args=[usern]))
        #follower, created = Follow.objects.get_or_create(user=visitor)
        #f#ollower.following.set([usern])
        #if not created:
            #follower.delete()
            #return HttpResponseRedirect(reverse('profile_page', args=[usern]))
        #follower.save()
        #return HttpResponseRedirect(reverse('profile_page', args=[usern]))
    try:
        f = Follow.objects.get(user=visitor, following=usern)
        return render(request, "network/profile_page.html", {
        "userv": usern,
        'posts': posts,
        "visitor": visitor,
        'follow': len(follow),
        'follows': len(follows),
        'f': f,
        'page_obj': page_obj,
        'likes': list_likes
    })
    except:
        return render(request, "network/profile_page.html", {
            "userv": usern,
            'posts': posts,
            "visitor": visitor,
            'follow': len(follow),
            'follows': len(follows),
            'page_obj': page_obj,
            'likes': list_likes
        })
    
@login_required    
def following(request):
    user =request.user
    user_id= user.id
    followings = Follow.objects.filter(user=user_id).all()
    posts_list = []
    for following in followings:
        userf = following.following.all()
        userf = userf[0]
        posts = NewPost.objects.filter(author=userf).all()
        posts = posts.order_by('-post_date').all()
        for post in posts:
            posts_list.append(post)
    likes = Like.objects.filter(user=request.user).all()
    list_likes = []
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    for like in likes:
        list_likes.append(like.post.pk)
    return render(request, "network/following.html", {
        'posts' : posts_list,
        'likes': list_likes,
        'page_obj': page_obj
    })

@csrf_exempt
def edit_post(request, id):
    post = get_object_or_404(NewPost, id=id)
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content')
        if content:
            post.text = content
            post.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Content is required.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})
