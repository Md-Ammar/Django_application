from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.forms.models import modelformset_factory # model form for query sets
from django.forms import ModelForm
from django.http import HttpResponse, Http404
from django.urls import reverse

from .forms import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient
# CRUD -> Create Retreive Update & Delete
# FBV -> CBV Function based : Class based

@login_required
def recipe_list_view(request):
    qs = Recipe.objects.filter(user=request.user)
    context = {
        "object_list": qs
    }
    return render(request, "recipes/list.html", context)

@login_required
def recipe_detail_view(request, id=None):
    hx_url = reverse("recipes:hx-detail", kwargs={'id': id})    
    context = {
        "hx_url": hx_url
    }
    return render(request, "recipes/detail.html", context)

@login_required
def recipe_detail_hx_view(request, id=None):
    if not request.htmx:
        raise Http404
    try:
        obj=Recipe.objects.get(id=id, user=request.user)
    except:
        obj=None
    if obj is None:
        return HttpResponse("Not found!")

    context = {
        "object": obj
    }
    return render(request, "recipes/partials/detail.html", context)


@login_required
def recipe_create_view(request):
    form = RecipeForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.htmx:
            headers = {
                "HX-Redirect": obj.get_absolute_url()
            }
            return HttpResponse("Created", headers=headers)
            # context={
            #     "object": obj
            # }
            # return render(request, "recipes/partials/detail.html", context)
        return redirect(obj.get_absolute_url())
    return render(request, "recipes/create-update.html", context)

@login_required
def recipe_update_view(request, id=None):
    obj = get_object_or_404(Recipe, id=id, user=request.user)
    form = RecipeForm(request.POST or None, instance=obj)
    new_ingredient_url = reverse("recipes:hx-ingredient-create", kwargs={"parent_id": obj.id})
    context = {
        "form": form,
        "object": obj,
        "new_ingredient_url": new_ingredient_url
    }
    if form.is_valid():
        form.save()
        context['message'] = 'Data Saved!'
    if request.htmx:
        return render(request, 'recipes/partials/forms.html', context)
    return render(request, "recipes/create-update.html", context)


@login_required
def recipe_ingredient_update_hx_view(request, parent_id=None, id=None):
    if not request.htmx:
        raise Http404
    try:
        parent_obj=Recipe.objects.get(id=parent_id, user=request.user)
    except:
        parent_obj=None
    print(parent_obj, parent_obj.id)
    if parent_obj is None:
        return HttpResponse("Not found!")

    instance = None
    if id is not None:    
        try:
            instance = RecipeIngredient.objects.get(recipe=parent_obj, id=id)
        except:
            print("instance not found")
            instance=None
    form = RecipeIngredientForm(request.POST or None, instance=instance)
    url = reverse("recipes:hx-ingredient-create", kwargs={"parent_id": parent_obj.id})
    if instance:
        url = instance.get_hx_edit_url()
    context = {
        "url": url,
        "form": form,
        "object": instance
    }
    if form.is_valid():
        new_obj = form.save(commit=False)
        if instance is None:# for add ingredient
            new_obj.recipe = parent_obj
        new_obj.save()
        context['object'] = new_obj
        return render(request, "recipes/partials/ingredient-inline.html", context)
    
    return render(request, "recipes/partials/ingredient-form.html", context)