from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect('/login')
    context = {'form':form}
    return render(request, "accounts/register.html", context)

# Create your views here.
def login_view(request):
    # future -> ?next=/articles/create/
    # if request.user.is_authenticated:
    #     return render(request, "accounts/already-logged-in.html", {})
    context={}
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        # username = request.POST.get("username")
        # password = request.POST.get("password")
        # # print(username, password) remove this
        # user = authenticate(request, username=username, password=password)
        # if user is None:
        #     context= {"error" :"Invalid username or password."}
        #     return render(request, "accounts.html", context)
        # print(user)
        # login(request, user)
        # return redirect('/')
    else:
        form = AuthenticationForm(request)
    context = {"form": form}

    return render(request, "accounts/login.html", context)
    
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("/login/")
    return render(request, "accounts/logout.html", {})
