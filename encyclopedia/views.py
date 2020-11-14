import markdown2
import random
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util

class SearchForm(forms.Form):
    page = forms.CharField(label="Search Encyclopedia")

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'style' : 'width: 40%;'}), label="Title")
    markdown = forms.CharField(label="Mark Down Text", widget=forms.Textarea(attrs={'class' : 'form-control', 'id': 'exampleFormControlTextarea1', 'style' : 'width: 80%;'}))

class EditPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'style' : 'width: 40%;', 'readonly': True}), label="Title")
    markdown = forms.CharField(label="Mark Down Text", widget=forms.Textarea(attrs={'class' : 'form-control', 'id': 'exampleFormControlTextarea1', 'style' : 'width: 80%;'}))

def methodPost(request):
    form = SearchForm(request.POST)
    if form.is_valid():
        page = form.cleaned_data["page"]
        return HttpResponseRedirect(f"/wiki/{page}")
    return None

def index(request):
    # Add code over here for the form input
    entries = util.list_entries()
    rand_page = random.choice(entries)
    if request.method == "POST":
        return methodPost(request)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": SearchForm(),
            "random": random.choice(util.list_entries())
        })

def entryPage(request, page):
    the_page =  util.get_entry(page)

    if request.method == "POST":
        if 'edit' in request.POST:
            return HttpResponseRedirect(f"/wiki/EditPage/{page}")
        else:
            return methodPost(request)
    if the_page == None:
        partial_entries = []
        for p in util.list_entries():
            if page.lower() in p.lower():
                partial_entries.append(p)
        return render(request, "encyclopedia/error.html",{
            "entries": partial_entries,
            "name": page,
            "form": SearchForm(),
            "random": random.choice(util.list_entries())
        })

    the_page = markdown2.markdown(the_page)
    return render(request, "encyclopedia/page.html",{
        "name": page,
        "page": the_page,
        "form": SearchForm(),
        "random": random.choice(util.list_entries())
    })

def newPage(request):
    if request.method == "POST":
        if 'search' in request.POST:
            return methodPost(request)
        form = NewPageForm(request.POST)
        if form.is_valid():
            entries = util.list_entries()
            if form.cleaned_data["title"] in entries:
                return render(request, "encyclopedia/NewPage.html",{
                    "error": True,
                    "form": SearchForm(),
                    "newpage": NewPageForm(request.POST),
                    "random": random.choice(util.list_entries())
                })
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["markdown"])
            page = form.cleaned_data["title"]
            return HttpResponseRedirect(f"/wiki/{page}")
    else: 
        return render(request, "encyclopedia/NewPage.html",{
            "form": SearchForm(),
            "newpage": NewPageForm(),
            "random": random.choice(util.list_entries())
        })

def editPage(request, page):
    if request.POST:
        if 'search' in request.POST:
            return methodPost(request)
        form = EditPageForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"], form.cleaned_data["markdown"])
            page = form.cleaned_data["title"]
            return HttpResponseRedirect(f"/wiki/{page}")
    else:
        edit = EditPageForm(initial={'title': page, 'markdown': util.get_entry(page)})
        return render(request, "encyclopedia/editpage.html", {
            "form": SearchForm(),
            "editpage": edit,
            "random": random.choice(util.list_entries())
        })
