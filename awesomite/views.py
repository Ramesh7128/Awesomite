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


