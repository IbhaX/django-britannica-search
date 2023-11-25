from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .utils import search
from .forms import SearchForm
from .models import Wiki

@login_required(login_url="login")
def home_view(request):
    template_name = "app/home.html"
    form = SearchForm()
    items = Wiki.objects.filter(user=request.user, content__isnull=False, content__gt='')
    return render(request, template_name, {'form': form, 'items': items})

@login_required(login_url="login")
def search_view(request):
    template_name = "app/home.html"  # Change the template name
    form = SearchForm()
    items = Wiki.objects.all()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['search']
            existing_items = Wiki.objects.filter(query__iexact=query.strip())
            if existing_items.exists():
                for existing_item in existing_items:
                    existing_item.user.add(request.user)
                responses = list(existing_items.values())
            else:
                responses = search(query)
                for item in responses:
                    new_wiki_item  = Wiki.objects.create(
                        title=item["title"],
                        content=item['content'],
                        summary=item["summary"],
                        image=item["image"],
                        query=query
                    )
                    new_wiki_item.user.add(request.user)
                items = Wiki.objects.filter(query__iexact=query.strip())
            return redirect("app:result", query=query)
    
    # If the form is not valid, still render the home template with the form and items
    return render(request, template_name, {'form': form, 'items': items})

@login_required(login_url="login")
def detail_view(request, pk):
    template_name = "app/wiki.html"
    item = Wiki.objects.get(id=pk)
    return render(request, template_name, {'item': item})


def result_view(request, query):
    items = Wiki.objects.filter(query=query).all()
    return render(request, 'app/results.html', {'items': items})