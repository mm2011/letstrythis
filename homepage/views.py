from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from DBapp.models import Question, Answer

# Create your views here.

#def quiz(request):
    #if request.user.is_authenticated:
        #allQuestions = Question.objects.all()
        #allAnswers = Answer.objects.all()
        #for q in allQuestions:
         #   for a in allAnswers:
         #       if q.questionID == a.questionID:



def donations(request):
    if request.user.is_authenticated:
        return render(request, 'homepage/donations.html')

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'homepage/login.html', {'message': None})
    else:
        context = {'user' : request.user}
        return render(request, 'homepage/index.html', context)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'homepage/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        #phone = request.POST['phone']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        #validate all fields have text

        emptyField = False
        Message = ""
        if first_name == "":
            emptyField = True
            Message = Message+"  'first name'  "
        if last_name == "":
            emptyField = True
            Message = Message+"  'last name'  "
        if email == "":
            emptyField = True
            Message = Message+"  'email'  "
        if username == "":
            emptyField = True
            Message = Message+"  'username'  "
        if password == "":
            emptyField = True
            Message = Message+"  'password'  "
        if password2 == "":
            emptyField = True
            Message = Message+"  'confirm password'  "
        if emptyField == True:
            print("The following cannot be empty:"+Message)
            messages.info(request, "The following cannot be empty:"+Message)
            return redirect('register')







        #validate if form fields are full
        if password == password2:
            if User.objects.filter(username = username).exists():
                print("Username already exists")
                messages.info(request, "Username already exists")
                return(redirect('register'))
            elif User.objects.filter(email = email).exists():
                print("This email is already registered")
                messages.info(request, "This email is already registered")
                return(redirect('register'))
            #elif User.objects.filter(phone = phone).exists():
                #print("This phone number is already registered")
                #messages.info(request, "This phone number is already registered")
                #return(redirect('register'))
            else:
                User.objects.create_user(first_name=first_name, last_name=last_name, email=email, #phone=phone,
                                     username=username, password=password)
                return render(request, 'homepage/login.html')
        else:
            print("Passwords do not match!")
            messages.info(request, "Passwords do not match")
            return redirect('register')
    else:
        return render(request, 'homepage/register.html')


