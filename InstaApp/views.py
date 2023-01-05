from django.shortcuts import render, redirect
from django.db import models
from .models import FollowersCount, LikePost, Profile, Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.contrib.auth.hashers import check_password, make_password
import random


# ---------------------------------------------  Home  -------------------------------------------

@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username = request.user.username)    # current user
    user_profile = Profile.objects.get(user = user_object)      # current user's data from profile model


    user_following_list = []                # list of the user that are following by login user
    feed = []                               # list of the users posts that are following by login user
    
    
    user_following = FollowersCount.objects.filter(follower = request.user.username)    # following users
    
    
    for users in user_following:
        user_following_list.append(users.user)          # Following
        
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user = usernames)      
        feed.append(feed_lists)                         # Following users posts
        
    # print(feed)
    
    #posts = Post.objects.filter(user = request.user.username)
    

    feed_list = list(chain(*feed))                      # takes multiple iterables and return one iterable

    # user suggestions ==>
    
    all_users = User.objects.all()
    user_following_all = []                 
    
    for user in user_following:
        user_list = User.objects.get(username = user.user)
        user_following_all.append(user_list)
        
    new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]      # neglecting following users

    current_user = User.objects.filter(username = request.user.username)        
    final_suggestions_list = [x for x in list(new_suggestions_list) if (x not in list(current_user))]
    # print(final_suggestions_list)
    random.shuffle(final_suggestions_list)
    
    username_profile = []
    username_profile_list = []
    
    for users in final_suggestions_list:
        username_profile.append(users.id)
        
    for ids in username_profile:
        profile_list = Profile.objects.filter(id_user = ids)
        username_profile_list.append(profile_list)
        
    suggestions_username_profile_list = list(chain(*username_profile_list))
    
    context = {
        'user_profile': user_profile, 
        'posts': feed_list, 
        'suggestions_username_profile_list': suggestions_username_profile_list[:4],
    }
    
    return render(request, "index.html", context)



# ---------------------------------------------  Sign Up  ----------------------------------------
def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Email Taken")
                return redirect("signup")
            elif User.objects.filter(username = username).exists():
                messages.info(request, "Username Taken")
                return redirect("signup")
            else:
                user = User.objects.create_user(username = username, email=email, password=password)
                user.save()
                 
                #login user and redirect to settings page
                user_login = authenticate(username = username, password = password)
                login(request, user_login)
                
                # create profile object for new user 
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model, id_user = user_model.id)
                new_profile.save()
                return redirect("/settings")
        else:
            messages.info(request, "Password not matching")
            return redirect("signup")
    else:
        return render(request, 'signup.html')
    
    
    
# ---------------------------------------------  Sign In  ----------------------------------------
def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        # pwd = make_password(password)
        user = authenticate(username = username, password = password)
        
        if user is not None:
            request.session["uid"] = user.id
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Invalid Credentials")
            return redirect("/signin")
    else:
        return render(request, 'signin.html')
    
    

# ---------------------------------------------  Explore & Search  ----------------------------------------
def explore(request):
    explore_feed = Post.objects.all()
    # print(explore_feed)
    return render(request, 'explore.html', {'explore': explore_feed})


def search(request):
    user_object = User.objects.get(username = request.user.username)        # Current User
    user_profile = Profile.objects.get(user = user_object)              # User's data from profile model
    
    if request.method == "POST":
        username = request.POST.get('username')                 
        username_object = User.objects.filter(username__icontains = username)       # getting searched person
        
        username_profile = []
        username_profile_list = []
        
        for users in username_object:
            username_profile.append(users.id)
            
        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user = ids)
            username_profile_list.append(profile_lists)
            
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'explore.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})


# --------------------------------------------- User Profile -------------------------------------------
@login_required(login_url="signin")
def profile(request, pk):
    user_object = User.objects.get(username = pk)               # requested user
    user_profile = Profile.objects.get(user=user_object)        # user profile
    user_posts = Post.objects.filter(user=pk)                   # posts of current user
    user_post_length = len(user_posts)                          # no. of posts of particular user
    
    follower = request.user.username                            
    user = pk 
    
    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_txt = 'Unfollow'
    else:
        button_txt = 'Follow'
        
    user_followers = len(FollowersCount.objects.filter(user = pk))          # follower's list
    user_following = len(FollowersCount.objects.filter(follower = pk))      # following list
        
        
    context = {
        'user_object': user_object, 
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_txt': button_txt,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)
    
    
    
# --------------------------------------------- Another User Profile -------------------------------------------
@login_required(login_url="signin")
def follow(request):
    if request.method == "POST":
        follower = request.POST["follower"]             # current user
        user = request.POST["user"]                     # search user's profile
        
        if FollowersCount.objects.filter(follower = follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user = user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect("/")    
    
    
    
# ---------------------------------------------  Posts -------------------------------------------
@login_required(login_url="signin")
def upload_post(request):
    
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image-upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()
        
        return redirect("/")
    else:
        return redirect("/")



# --------------------------------------------- Liked Posts -------------------------------------------
@login_required(login_url="signin")
def like_post(request):
    username = request.user.username 
    post_id = request.GET.get("post_id")
    
    post = Post.objects.get(id = post_id)
    
    like_filter = LikePost.objects.filter(post_id = post_id, username=username).first()
    
    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect("/")
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect("/")
    
    
    
# ---------------------------------------------  Settings  ---------------------------------------
@login_required(login_url="signin")
def Settings(request):
    user_profile = Profile.objects.get(user = request.user)
    
    if request.method == "POST":
        
        if request.FILES.get('image') == None:
            name = request.POST['name']
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.name = name
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        if request.FILES.get('image') != None:
            name = request.POST['name']
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.name = name
            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        return redirect('/settings')
    else:       
        return render(request, "settings.html", {'user_profile': user_profile})
    
    
@login_required(login_url="signin")
def Password_reset(request):
    user_pwd = request.user.password        # fetch current user's password
    # print(user_pwd)
    if request.method == "POST":
        pwd = request.POST["pwd"]
        pwd2 = request.POST["pwd2"]
        
        if pwd == pwd2:
            matching_pwd = check_password(pwd, user_pwd)       # check_password function to match the hash pwd & entered pwd
            # print(matching_pwd)
            if matching_pwd == False:            
                user = request.user                     # fetching current user
                pd = make_password(pwd)                 # making password hashable(encrypt) using make_pwd fun to store in db 
                # print(pd)  
                user.password = pd                   # set entered 'pwd' to the user's password field
                user.save(update_fields = ['password'])         # saving the particular field using update_fields in models 
                messages.success(request, "Password changed successfull!")
                return render(request, "pwdreset.html")
            else:
                messages.error(request, "Seems you've entered old password!")
                return render(request, "pwdreset.html")
        else:
            messages.error(request, "Password doesn't match!")
            return render(request, "pwdreset.html")
    else:
        user_profile = Profile.objects.all()
        context = {'user_profile': user_profile}
        return render(request, 'pwdreset.html', context)
    
    
# ---------------------------------------------  Log out  ----------------------------------------   
@login_required(login_url="signin")
def UserLogout(request):
    logout(request)
    return redirect("/signin")

