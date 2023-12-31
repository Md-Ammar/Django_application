from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required

from .forms import ArticleForm
from .models import Article


# Create your views here.

def article_search_view(request):
    query = request.GET.get("q") # this returns a dictionary
    qs = Article.objects.search(query=query)
    context={
        "object_list": qs,
    }
    return render(request, "articles/search.html", context=context)

#@csrf_exempt
@login_required
def article_create_view(request):
    article_object=None
    form=ArticleForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        article_object = form.save()
        context['form'] = ArticleForm() # (rerender) to clear out that day to prevent spamming same
        # return redirect("article-detail", slug=article_object.slug)
        return redirect(article_object.get_absolute_url())
        # context['object'] = article_object
        # context['created'] = True
    else:
        print(form.errors)
    return render(request, "articles/create.html", context=context)

# def article_create_view(request):
#     # print(request.POST)
#     article_object=None
#     form=ArticleForm()
#     context = {
#         "form": form,
#     }
    
#     if request.method == "POST":
#         form = ArticleForm(request.POST)
#         context['form'] = form
#         if form.is_valid():
#             title = form.cleaned_data.get('title')
#             content = form.cleaned_data.get('content')
#             print(title, content)
#             article_object = Article.objects.create(title=title, content=content)
#             context['object'] = article_object
#             context['created'] = True

#     return render(request, "articles/create.html", context=context)


def article_detail_view(request, slug=None):
    article_obj = None
    if id is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except:
            raise Http404

    context = {
        "object": article_obj,
    }
    return render(request, "articles/details.html", context=context)
