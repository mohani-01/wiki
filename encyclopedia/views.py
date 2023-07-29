
from django.http import HttpResponse, HttpResponseRedirect


from django.shortcuts import render
from django.urls import reverse

from markdown2 import Markdown
from . import util
from .forms import CreateNewWiki
from random import randrange


# Used to change markdown to html
markit = Markdown()


def index(request):
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })


def page(request, name):
    # Get the content if exist
    content = util.get_entry(name)

    if content:
        # Return the page and convert markdown to html
        return render(request, "encyclopedia/title.html", {
            "title": name.capitalize(),
            "body": markit.convert(content)
        })

    else:
        return render(request, "encyclopedia/error.html")


def search(request):

    if request.method == "POST":
        # Get the value of user search 
        title = request.POST.getlist("q")[0]


        # Get the content if exist
        content = util.get_entry(title)

        if content:
            return render(request, "encyclopedia/title.html", {
                "title": title.capitalize(),
                "body": markit.convert(content),
            })

        # if the content doesn't exist  
        else:
            # Get all the entries
            all_pages = util.list_entries()
            # Similar pages
            similar_pages = []

            # search if there is similarity b/n them 
            for page in util.list_entries():

                # Check if the substring is in the pages
                if title.lower() in page.lower():
                    similar_pages.append(page)

            # display all of them
            return render(request, 'encyclopedia/search.html', {
                "search": similar_pages,
            })
    # via GET ( for safety)
    else:
        return index(request)

def add(request):
    # via POST
    if request.method == "POST":

        # Get all the information the user insert
        form = CreateNewWiki(request.POST)

        # Check if the form is valid
        if form.is_valid():
            # GET the title and check if the same title exist
            title = form.cleaned_data["title"]
            if util.get_entry(title):
                # Return error message
                return HttpResponse("<h1>There is another title by this name.</h1>")
            
            # Else get the content 
            content = form.cleaned_data["content"]

            # add it to the database
            util.save_entry(title, content)
            
            # Return the user into entry page
            return HttpResponseRedirect(reverse('wiki:index '))

    # via GEt
    else:
       # return empty form to the user
        return render(request, 'encyclopedia/addpage.html', {
            "form": CreateNewWiki(),
        })


def random(request):
    # GET all the topics
    topics = util.list_entries()

    # random number
    l = randrange(0, len(topics))
    
    # get the title randomly
    title = util.get_entry(topics[l])

    # return that page
    return render(request, 'encyclopedia/title.html', {
        "title":  topics[l],
        "body": markit.convert(title)
    })


def edit(request, file):
    if request.method == "POST":

        # Get the update data
        update = CreateNewWiki(request.POST)
        
        # Clean the data and update it to the database
        if update.is_valid():
            content = update.cleaned_data['content']
            util.save_entry(file, content)
            
            # return them to new entry page
            return HttpResponseRedirect(reverse('wiki:index'))

        # if the data is not valid return to the user edited data
        else:
            return render(request,'encyclopedia/edit.html', {
                "title":file,
                "edit": update,
            })

    # via Get
    else:
        
        # Get the topic and populate it with existing data: file= title of the page, util.get_entry(file) is text w/ markdown font-type
        topic = CreateNewWiki(initial={'title': file, 'content': util.get_entry(file)})
        # Make the title page readonly so the user can't edit
        # Its a distruction, so that even if this attribute is change it has no meaning untill the form action is unchange
        topic.fields['title'].widget.attrs['readonly'] = True
      
        # The return the data to the user
        return render(request, 'encyclopedia/edit.html', {
            "title": file,
            "edit": topic,
        })
