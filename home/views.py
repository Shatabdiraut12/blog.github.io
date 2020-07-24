# redirect import for signup
from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact  # for store into the db
from django.contrib import messages  # for show alert meassages
from django.contrib.auth import authenticate, login, logout  # for login logout
# for create user which is present in admin panel already so we do .models
from django.contrib.auth.models import User
from blog.models import Post  # for search

# html pages


def home(request):
    return render(request, 'home/home.html')


def contact(request):
    #messages.error(request, 'Welcome to Contact')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()  # by write this line it will come in db or store in db
            messages.success(
                request, "Your message has been successfully sent")
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')


def search(request):
    query = request.GET['query']
    # query is a string so we write len
    if len(query) > 70:
        allPosts = Post.objects.none()  # to set empty query
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent, allPostsAuthor)

    if allPosts.count() == 0:  # here for query we werite count not length
        messages.warning(request, "No search results found")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)

# authentication APIs


def handleSignup(request):
    if request.method == 'POST':
        # GET the post paramaters like username, firstname , lastname etc...
        # request.post is a dictonary jismain we create value
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errornous input
        # username should under 5 characters
        if len(username) > 5:
            messages.error(request, "Username must be under 5 characters")
            return redirect('home')

        # for username is alphanumeric means abc123
        if not username.isalnum():
            messages.error(
                request, "Username should only contain letters and numbers")
            return redirect('home')

        # passwords should match
        if pass1 != pass2:
            messages.error(request, "Password do not match")
            return redirect('home')

        # create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('home')  # means redirect in home

    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        # get the post parameters like username n password
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        # we will do authentecate
        user = authenticate(username=loginusername, password=loginpassword)

        # if user is not none means username n password was correct which given during signup
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials, PLease try again")
            return redirect('home')

    return HttpResponse("404 - Not found")


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')
