# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from awesomite.models import tasks
from awesomite.forms import todoform
import urllib
import json
from bs4 import BeautifulSoup
import csv

def index(request):
    context = RequestContext(request)

    #######################
    #for top 10 music list
    html_doc = urllib.urlopen("https://www.youtube.com/playlist?list=PLFgquLnL59akA2PflFpeQG9L01VFg90wS")
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
    list = tasks.objects.all()
    context_dict['todolist'] = list

    return render_to_response('awesomite/index.html', context_dict, context)


def addtodo(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = todoform(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect()
            return index(request)
        else:
            print form.errors
    else:
        form = todoform()



    return render_to_response('awesomite/index.html', {'form':form}, context)
