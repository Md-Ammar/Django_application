"""To render html pages"""
import random
from django.http import HttpResponse
from articles.models import Article
from django.template.loader import render_to_string, get_template

def home_view(request, *args, **kwargs):
    article_obj = Article.objects.get(id=3)
    query_set = Article.objects.all()# returns query set
    
    #templates

    # another way
    # tmpl = get_template("home-view.html")
    # tmpl.string = tpl.render(context=context)
    # my_list = [1, 35,2, 14,52,235, 25]
    
    context = {
        "object_list": query_set, 
        "title": article_obj.title,
        "content": article_obj.content,
        "id": article_obj.id,

    }


    HTML_STRING = render_to_string("home-view.html", context=context)
    # HTML_STRING = """
    # <h1>{title} ({id})!</h1>
    # <p>{content}!</p>
    # """.format(**context)
    return HttpResponse(HTML_STRING)