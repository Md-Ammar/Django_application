from django.shortcuts import render

from articles.models import Article
from recipes.models import Recipe

SEARCH_TYPE_MAPPING = {
    'article': Article,
    'articles': Article,
    'recipe': Recipe,
    'recipes': Recipe
}


# Create your views here.
def search_view(request):
    query = request.GET.get('q')
    search_type = request.GET.get('type')
    Klass = Recipe # default
    if search_type in SEARCH_TYPE_MAPPING.keys():
        Klass = SEARCH_TYPE_MAPPING[search_type]
    qs = Klass.objects.search(query=query)
    context = {
        "queryset": qs,
    }
    template = "search/results-view.html"
    if request.htmx:
        template = "search/partials/results.html"    
    return render(request, template, context=context)
