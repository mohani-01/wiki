from django import forms
from django.http import HttpResponse

from django.shortcuts import render

from markdown2 import Markdown
from . import util
import random

markit = Markdown()
class CreateNewWiki(forms.Form):
    title = forms.CharField(label="Title", max_length=100, 
                    widget=forms.TextInput(attrs={'placeholder': 'Search'}))
    # content = forms.Textarea(label="Content", attrs={'type': 'markdwo'}) 
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Content in markdown format \
                                                           ## Django \
                                                           # Django is python FrameWork for backend development. '}))
    


def index(request):
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })


def find(request, name):
    title = util.get_entry(name)
    if title:
        return render(request, "encyclopedia/title.html", {
            "title": name.capitalize(),
            "body": markit.convert(title)
        })
    else:
        return render(request, "encyclopedia/error.html")


def search(request):
    if request.method == "POST":
        title = request.POST.getlist("q")[0]
        topic = util.get_entry(title)

        if topic:
            return render(request, "encyclopedia/title.html", {
                "title": title.capitalize(),
                "body": markit.convert(topic),
            })
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
    else:
        return index(request)

def add(request):
    if request.method == "POST":
        form = CreateNewWiki(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title):
                return HttpResponse("There is another title by this name.")
            content = form.cleaned_data["content"]
        print(content)
        # util.save_entry(title, content)
        return HttpResponse("Working on it")
    
    else:
        form = CreateNewWiki()

        return render(request, 'encyclopedia/addpage.html', {
            "form": form,
        })

def randomm(request):
    topics = util.list_entries()
    l = random.randrange(0, len(topics))
    title = util.get_entry(topics[l])
    return render(request, 'encyclopedia/title.html', {
        "title":  topics[l],
        "body": markit.convert(title)
    })


def edit(request, file):
    if request.method == "POST":
        return HttpResponse("Done!")


    else:
        topic = CreateNewWiki(initial={'title': file, 'content': util.get_entry(file)})

            # editForm = editPage(initial={'title': name, 'textContent': util.get_entry(name)})

    # topic = util.get_entry(file)
    # editfile = CreateNewWiki(topic)
        return render(request, 'encyclopedia/edit.html', {
            "title": file,
            "edit": topic,
        })
    return HttpResponse("Hello, World")