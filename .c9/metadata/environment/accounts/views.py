{"filter":false,"title":"views.py","tooltip":"/accounts/views.py","ace":{"folds":[],"scrolltop":477.7778015136719,"scrollleft":0,"selection":{"start":{"row":0,"column":0},"end":{"row":73,"column":110},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"hash":"e009c6656fce6f007118fabdf6ae7f9b8b1e1be6","undoManager":{"mark":-1,"position":-1,"stack":[[{"start":{"row":0,"column":0},"end":{"row":73,"column":110},"action":"remove","lines":["from django.shortcuts import render, redirect, reverse","from django.contrib import auth, messages","from django.contrib.auth.decorators import login_required","from accounts.forms import UserLoginForm, UserRegistrationForm","from django.contrib.auth.models import User","from tickets.models import Ticket","","# Create your views here.","def index(request):","    \"\"\" Return the index.html file \"\"\"","    return render(request, 'tickets.html')","    ","@login_required    ","def logout(request):","    \"\"\" Log the user out \"\"\"","    auth.logout(request)","    messages.success(request, \"You have successfully been logged out!\")","    return redirect(reverse('index'))","    ","    ","def login(request):","    \"\"\" Return a login page \"\"\"","    if request.user.is_authenticated:","        return redirect(reverse('index'))","    if request.method == 'POST':","        login_form = UserLoginForm(request.POST)","        ","        if login_form.is_valid():","            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])","            ","            if user:","                auth.login(user=user, request=request)","                messages.success(request, \"You have successfully logged in!\")","                return redirect(reverse('index'))","            else:","                login_form.add_error(None, \"Your username or password is incorrect\")","    else:","        login_form = UserLoginForm()","    return render(request, 'login.html', {'login_form': login_form})","    ","    ","def registration(request):","    \"\"\" Render the registration page \"\"\"","    if request.user.is_authenticated:","        return redirect(reverse('index'))","        ","    if request.method =='POST':","        registration_form = UserRegistrationForm(request.POST)","        ","        if registration_form.is_valid():","            registration_form.save()","            ","            user = auth.authenticate(username=request.POST['username'],","                                        password=request.POST['password1'])","                                        ","            if user:","                auth.login(user=user, request=request)","                messages.success(request, \"You have successfully registered\")","                return redirect(reverse('index'))","        else:","            messages.error(request, \"Unable to register your account at this time\")","    else:","        registration_form = UserRegistrationForm()","        ","    return render(request, 'registration.html', ","                    {'registration_form': registration_form})","                    ","                    ","def profile(request):","    \"\"\" The user's profile page \"\"\"","    user = User.objects.get(email=request.user.email)","    bugs = Ticket.objects.filter(creator=user.username, ticket_type='Bug').count()","    feature_requests = Ticket.objects.filter(creator=user.username, ticket_type='Feature Request').count()","    return render(request, 'profile.html', {'user': user, 'bugs': bugs, 'feature_requests': feature_requests})"],"id":2},{"start":{"row":0,"column":0},"end":{"row":0,"column":41},"action":"insert","lines":[" python3 manage.py runserver 0.0.0.0:8080"]}]]},"timestamp":1565115346646}