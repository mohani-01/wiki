from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from markdown2 import Markdown
from . import util

markit = Markdown()



def index(request):
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })


        
    # return HttpResponse(f"Hello, {to} Done!")

def find(request, name):

    title = util.get_entry(name)
    if title:
        return render(request, "encyclopedia/title.html", {
            "title": name.capitalize(),
            "body": markit.convert(title)
        })
    else:
        return render(request, "encyclopedia/error.html")
    # return HttpResponse(f"Hello, {name.capitalize()}!")

def search(request):
    if request.method == "POST":
        title = request.POST.getlist("q")[0]

        topic = util.get_entry(title)
        if topic:
            return render(request, "encylopedia/title.html", {
                "title": title.capitalize(),
                "body": markit.convert(topic),
            }
            )

        else:
            # Get all the entries
            all_pages = util.list_entries()
            
            # Similar pages
            similar_pages = []

            # search if there is similarity b/n them 
            for page in util.list_entries():
                if title.lower() in page.lower():
                    similar_pages.append(page)
                

            # display all of them
            return render(request, 'encyclopedia/search.html', {
                "search": similar_pages,
            })

            # return HttpResponse("Working on it!")
        
    else:
        return index(request)