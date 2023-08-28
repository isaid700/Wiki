from django.shortcuts import render
from django.core.files.storage import default_storage
from . import util
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
from .util import save_entry, get_entry
import random

# defines a page where the entries are listed. The "home" page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# defines a redirect for the link from the entries to their markdown pages
def redirect(request, name):
    try:
        f = default_storage.open(f"entries/{name}.md")
        content = f.read().decode("utf-8")
        edit_url = reverse("edit", args=[name])  # Get the URL for the edit page
        edit_button = f'<a href="{edit_url}" style="background-color: white; color: blue; padding: 5px 10px; border-radius: 5px; margin-left: 30px">Edit</a>' # Create the edit button HTML
        content_with_edit_button = content + edit_button  # Combine the content and edit button HTML
        return HttpResponse(content_with_edit_button)
    except FileNotFoundError:
        return render(request, "index.html", {
            "name": name.capitalize()
        })

#Function for the search bar
def search(request):
    query = request.GET.get('q')
    if query:
        entries = util.list_entries()
        search_results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/searchresults.html", {
            "query": query,
            "search_results": search_results
        })
    else:
        return redirect('index')
    
#function for  the search results page
def search_results(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    search_results = [entry for entry in entries if query.lower() in entry.lower()]
    return render(request, "searchresults.html", {
        "query": query,
        "search_results": search_results
    })

#creating a class for the form
class NewForm(forms.Form):
    addpage = forms.CharField(label="")


#Allow the form to create a new page
def createnew(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            addpage = form.cleaned_data["addpage"]
            
            # Check if the entry already exists
            if util.get_entry(addpage) is not None:
                return render(request, "encyclopedia/error.html", {
                    "form": form,
                    "error_message": "An entry with the same title already exists."
                })
            
            # Save the new entry
            util.save_entry(addpage, "Click the Edit button to add content to this page!")
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "encyclopedia/createnew.html", {
                "form": form
            })

    return render(request, "encyclopedia/createnew.html", {
        "form": NewForm()
    })

class EditForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea())

#Performs an edit on 
def edit(request, name):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            save_entry(name, content)  
            return redirect("redirect", name=name)
        
#Checks to see if the input exists and if not returns an error. 
    page = util.get_entry(name)
    if page is None:
        return render(request, "error.html", {
            "error_message": "Entry does not exist."
        })

    form = EditForm(initial={"content": page})
    return render(request, "encyclopedia/edit.html", {
        "name": name,
        "form": form,
        "content": page
    })

#for the random page function
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('redirect', name=random_entry)

    