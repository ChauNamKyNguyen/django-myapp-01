# From Django
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate, login, logout

# login_required is a decorator in python
# decorator is a function to change a function of a function 
# without editing the source code
# change setting.put LOGIN_URL to 
# redirect user when he/she doesn't log in
from django.contrib.auth.decorators import login_required

# My models
from jav.models import Movie, Actress, UserProfile

# My forms
from jav.forms import ActressForm, MovieForm
from jav.forms import UserForm, UserProfileForm

# Utility
import re, json
from datetime import datetime

# Create your views here.
def index(request):
    context_dict = {}
    # Get top ten like of movie
    actress_list = Actress.objects.order_by('-like')[:10]    
    context_dict['actresses'] = actress_list
    
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, we default to zero and cast that.
    # visits = int(request.COOKIES.get('visits', '1'))
    
    # Session solution
    visits = request.session.get('visits')
    if not visits:
        visits = 1
        
    reset_last_visit_time = False
    
    # User login
    if request.user.is_authenticated:
        userprofile = UserProfile.objects.get(user=request.user)
        context_dict['userprofile'] = userprofile   
    
    
    
    # if 'last_visit' in request.COOKIES:
        # last_visit = request.COOKIES['last_visit']
        # last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
    
    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")    
    
        if (datetime.now() - last_visit_time).seconds > 5:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
        
    context_dict['visits'] = visits
        
    response = render(request, 'jav/index.html', context_dict)
        
    if reset_last_visit_time:
        # response.set_cookie('last_visit', datetime.now())
        # response.set_cookie('visits', visits)
        
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
        
    # Render data
    return response

def about(request):
    return render(request, 'jav/about.html', {})

def view_actress(request, name):
    context_dict = {}
    
    try:
        actress = Actress.objects.get(slug = name)
        context_dict['actress_name'] = actress.name
        
        movies = Movie.objects.filter(actress=actress)
        
        context_dict['movies'] = movies
        context_dict['actress'] = actress
    except Actress.DoesNotExist:
        pass
        
    return render(request, 'jav/actress.html', context_dict)

# Create a new actress
@login_required
def add_actress(request):
    if request.method == 'POST':
        form = ActressForm(request.POST)
        
        if form.is_valid():
            actress = form.save(commit=False)
            
            # Upload file
            if 'image' in request.FILES:
                actress.image = request.FILES['image']
            
            actress.save()
            
            # Return the page 'index'
            return index(request)
        else:
            # Error handling
            print (form.errors)
    else:
        # Not POST, display again
        form = ActressForm()
        
    return render(request, 'jav/add_actress.html', {'form': form})    

# Create a new movie
@login_required
def add_movie(request, name):
    try:
        actress = Actress.objects.get(slug=name)
    except Actress.DoesNotExist:
        actress = None
        
    context_dict = {}    
    
    if request.method == 'POST':
        form = MovieForm(request.POST)
        
        if form.is_valid():
            if actress:
                movie = form.save(commit=False)
                movie.actress = actress
                movie.views = 0
                movie.like = 0
                movie.date = datetime.now()
                movie.save()
                
                return redirect('/jav/actress/{0}'.format(actress.slug))
        else:
            print(form.errors)
    else:
        form = MovieForm()
        
    context_dict['actress_name_slug'] = actress.name
    context_dict['form'] = form
    context_dict['actress'] = actress
    return render(request, 'jav/add_movie.html', context_dict)

# User register
def register(request):
    registered = False
    
    if request.session.test_cookie_worked():
        print(">>> TEST COOKIE WORKED!")
        request.session.delete_test_cookie()
    else:
        print(">>> COOKIE NOT WORK")
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Save data into database
            user = user_form.save()
            
            # Hash password then save into database again
            user.set_password(user.password)
            user.save()
            
            # Set 'commit' to False to avoid saving to database
            # We need to update user's attributes before saving 
            profile = profile_form.save(commit=False)
            profile.user = user
            
            # Did user provide picture ?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                
            profile.save()
            
            # Auto login
            user = authenticate(username=user.username, password=user.password)
            if user:
                login(request, user)

            # Register successfully
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()        
        
    
    return render(request, 'jav/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})    

# User log in
def user_login(request):
    if request.method == 'POST':
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user:
            # Login successfully
            if user.is_active:
                # User is enable
                login(request, user)
                
                # Get avatar so it can display in all sites
                userprofile = UserProfile.objects.get(user=request.user)
                request.session['avatar_url'] = userprofile.picture.url   
                
                return HttpResponseRedirect('/jav/')
            else:
                # User is disable
                return HttpResponse('Your account is disabled')
        else:        
            # Login fail
            print("Invalid login detail: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied")
    else:
        # No submit, so do nothing
        return render(request, 'jav/login.html', {})   

@login_required
def restricted(request):
    return render(request, 'jav/restricted.html', {}) 

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/jav')
    
@login_required
def like_actress(request):
    actress_id = None
    if request.method == 'GET':
        actress_id = request.GET['actress_id']   

    likes = 0
    if actress_id:
        actress = Actress.objects.get(id=int(actress_id))
        if actress:
            likes = actress.like + 1
            actress.like = likes
            actress.save()
    
    return HttpResponse(likes)   

# Test AJAX
def more_todo(request):
    if request.is_ajax():
        todo_items = ['Mow Lawn', 'Buy Groceries',]
        data = json.dumps(todo_items)
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404

def add_todo(request):
    if request.is_ajax() and request.method == 'POST':
        print("Come here")
        data = {'message': "%s added" % request.POST.get('item')}
        return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        raise Http404    