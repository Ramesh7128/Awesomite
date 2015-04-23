# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from awesomite.models import tasks
from awesomite.forms import todoform
import urllib
from django.http import HttpResponseRedirect
import json
from bs4 import BeautifulSoup
import csv
import smtplib
from awesomite.forms import Userform, Userprofileform
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def index(request):
    context = RequestContext(request)

    #######################
    #for top 10 music list
    #######################

    html_doc = urllib.urlopen("https://www.youtube.com/playlist?list=PLrEnWoR732-BHrPp_Pm8_VleD68f9s14-")
    soup = BeautifulSoup(html_doc)
    musiclist = []
    urllist = []
    urllist1 = []
    context_dict = {}
    links = soup.find_all('tr', limit = 10)
    url1 = "https://www.youtube.com/embed/"
    for link in links:
        musiclist.append(link.get('data-title'))
        urllist1.append(url1+link.get('data-video-id'))
    # urls = soup.find_all('a')

    # url1 = "https://www.youtube.com/embed/"
    # for link in urls:
    #     if link.parent.name == 'td' and len(urllist1)<10:
    #          urllist.append(url+link.get('href'))
    #         # urllist1.append(url1+link.get('href'))
    master = zip(musiclist,urllist1)
    context_dict['top100music'] = master

    #########################
    #for todo list
    #########################

    if request.method == 'POST':
        if 'submit' in request.POST:
            form = todoform(request.POST)

            if form.is_valid():

                task = form.save(commit=False)
                try:
                    user = User.objects.get(username=request.user)
                    task.user = user
                    task.save()
                    #######################
                    content = task.description
                    mail = smtplib.SMTP('smtp.gmail.com', 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login('ramesh7128@gmail.com','********')
                    mail.sendmail('ramesh7128@gmail.com', 'ramesh7128@gmail.com', content)
                    mail.close()
                    ########################
                    return HttpResponseRedirect("/awesomite/")
                except User.DoesNotExist:
                    context_dict['nouser'] = "please login"



                # return HttpResponseRedirect("/awesomite/")
            else:
                print form.errors
        elif 'del' in request.POST:
            title = request.POST.get('title')
            tasks.objects.filter(title=title).delete()
            return HttpResponseRedirect("/awesomite/")

    else:
        form = todoform()
    context_dict['form'] = form
    try:
        usercheck = User.objects.get(username=request.user)
        list = tasks.objects.filter(user=usercheck)
        context_dict['todolist'] = list

    except:
        pass

    return render_to_response('awesomite/index.html', context_dict, context)


def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = Userform(data=request.POST)
        profile_form = Userprofileform(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()
            registered =True

        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = Userform()
        profile_form = Userprofileform()

    return render_to_response('awesomite/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/awesomite/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('awesomite/login.html', {}, context)

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/awesomite/')
