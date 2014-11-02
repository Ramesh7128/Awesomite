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
from awesomite.forms import Userform, Userprofileform

def index(request):
    context = RequestContext(request)

    #######################
    #for top 10 music list
    #######################

    html_doc = urllib.urlopen("https://www.youtube.com/playlist?list=PLrEnWoR732-BHrPp_Pm8_VleD68f9s14-")
    soup = BeautifulSoup(html_doc)
    musiclist = []
    urllist = []
    context_dict = {}
    links = soup.find_all('tr', limit = 10)
    for link in links:
        musiclist.append(link.get('data-title'))
    urls = soup.find_all('a')
    url = "https://www.youtube.com"
    for link in urls:
        if link.parent.name == 'td' and len(urllist)<10:
            urllist.append(url+link.get('href'))
    master = zip(musiclist,urllist)
    context_dict['top100music'] = master

    #########################
    #for todo list
    #########################

    if request.method == 'POST':
        if 'submit' in request.POST:
            form = todoform(request.POST)

            if form.is_valid():
                form.save(commit=True)
                return HttpResponseRedirect("/awesomite/")
            else:
                print form.errors
        elif 'del' in request.POST:
            title = request.POST.get('title')
            tasks.objects.filter(title=title).delete()
            return HttpResponseRedirect("/awesomite/")

    else:
        form = todoform()
    context_dict['form'] = form
    list = tasks.objects.all()
    context_dict['todolist'] = list

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

    return render_to_response('rango/register', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)



