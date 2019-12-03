from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from DBapp.models import Question, Answer
from .models import People, Score



# Create your views here.
def saveBio(request):
    if request.method == 'GET':
        bioInput = request.GET['bio']
        obj = People.objects.get(username=request.user.username)
        obj.bio = bioInput
        obj.save()
        result = "Saved!"
        return HttpResponse(result)

def getScore(request):
    if request.method == 'GET':
        quizlist = Score.objects.filter(username=request.user.username).order_by('-id')
        currentScore = quizlist[0]
        context = {'quizlist' : quizlist, 'username' : request.user.username, 'currentScore' : currentScore}
        return render(request, 'homepage/getScore.html', context)


def isCorrect(request):
    if request.method == 'GET':
        answer = request.GET['answer']
        answerID = request.GET['answerID']
        answerTemp = Answer.objects.get(answerText=answer, questionID=answerID)
        quizID = request.GET['quizID']
        #numQuestions = request.GET['numQuestions']
        if answerTemp.isRight:
            obj = Score.objects.get(id=quizID)
            obj.numCorrect = obj.numCorrect + 1
            obj.save()
            return HttpResponse("You are correct!")
        else:
            return HttpResponse("Incorrect.")
    else:
        return HttpResponse("Method was not a GET")


def checkLogin(request):
    if request.method == 'GET':
        checkUser = request.GET['checkUser']
        checkPass = request.GET['checkPass']
        user = auth.authenticate(username=checkUser, password=checkPass)
        if user is not None:
            return HttpResponse(True)
        else:
            return HttpResponse(False)
    else:
        return redirect('homepage/login.html')


def quiz(request):
    if request.user.is_authenticated:
        qSet = Question.objects.all()
        size = 0
        for q in qSet:
            size += 1


        Score.objects.create(username=request.user.username, numQuestions=size, numCorrect=0)
        obj = Score.objects.filter(username=request.user.username).order_by('-id')[0]

        context = {'questions': Question.objects.all(), 'answers': Answer.objects.all(), 'quizID' : obj.id}
        return render(request, 'homepage/quiz.html', context)


def donations(request):
    if request.user.is_authenticated:
        return render(request, 'homepage/donations.html')


def index(request):
    if not request.user.is_authenticated:
        return render(request, 'homepage/login.html', {'message': None})
    else:
        userBio = People.objects.get(username=request.user.username)
        context = {'user': request.user, 'userBio' : userBio.bio}
        return render(request, 'homepage/index.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            #person = People.objects.get(username=username)
            #person.currentUser=True
            #person.save(['currentUser'])
            return redirect('index')
        else:
            print("Invalid credentials")
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'homepage/login.html')


def logout(request):
    auth.logout(request)
    #person = People.objects.get(currentUser=True)
    #person.currentUser=False
    #person.save(['currentUser'])
    return redirect('login')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        # validate all fields have text

        emptyField = False
        Message = ""
        if first_name == "":
            emptyField = True
            Message = Message + "  'first name'  "
        if last_name == "":
            emptyField = True
            Message = Message + "  'last name'  "
        if email == "":
            emptyField = True
            Message = Message + "  'email'  "
        if username == "":
            emptyField = True
            Message = Message + "  'username'  "
        if password == "":
            emptyField = True
            Message = Message + "  'password'  "
        if password2 == "":
            emptyField = True
            Message = Message + "  'confirm password'  "
        if emptyField == True:
            print("The following cannot be empty:" + Message)
            messages.info(request, "The following cannot be empty:" + Message)
            return redirect('register')

        # input scrubbing for security

        # first and last name validation
        nameban = "!@#$%^&*()_+=-0987654321?/.>,<{}[];:\'\"|`~"
        for i in range(len(first_name)):
            for b in range(len(nameban)):
                if first_name[i] == nameban[b]:
                    print("You can only use appropriate characters for your first name. letter: " + nameban[b])
                    messages.info(request,
                                  "You can only use appropriate characters for your first name. letter: " + nameban[b])
                    return redirect('register')

        for i in range(len(last_name)):
            for b in range(len(nameban)):
                if last_name[i] == nameban[b]:
                    print("You can only use appropriate characters for your first name. letter: " + nameban[b])
                    messages.info(request,
                                  "You can only use appropriate characters for your last name. letter: " + nameban[b])
                    return redirect('register')
        # email validation
        emailban = ("!#$%^&*()=+\|]}[{\'\";:?/><,`~")
        valid = 0
        for i in range(len(email)):
            if email[i] == '@':
                valid += 1
            if email[i] == '.':
                valid += 1
            for b in range(len(emailban)):
                if email[i] == emailban[b]:
                    print("Your email is not the proper format. Code injection free zone!")
                    messages.info(request, "Your email is not the proper format. Code injection free zone!")
                    return redirect('register')
        if valid < 2:
            print("Your email is not the proper format. Code injection free zone!")
            messages.info(request, "Your email is not the proper format. Code injection free zone!")
            return redirect('register')
        # username validation
        usernameban = "!@#$%^&*()=+\|]}[{\'\";:?/><,`~"
        for i in range(len(username)):
            for b in range(len(usernameban)):
                if username[i] == usernameban[b]:
                    print("You can only use appropriate characters for your username. letter: " + usernameban[b])
                    messages.info(request,
                                  "You can only use appropriate characters for your username. letter: " + usernameban[
                                      b])
                    return redirect('register')
        # password validation
        passban = "\'\"><.,?/;:{}[]=)(*`~"
        allowedSpecials = "!@#$%^&"
        for i in range(len(password)):
            for b in range(len(passban)):
                if password[i] == passban[b]:
                    print("You can only use appropriate characters for your password. Allowed special characters: "
                          + allowedSpecials)
                    messages.info(request,
                                  "You can only use appropriate characters for your password. Allowed special characters: "
                                  + allowedSpecials)
                    return redirect('register')

        # validate fields
        if password == password2:
            if User.objects.filter(username=username).exists():
                print("Username already exists")
                messages.info(request, "Username already exists")
                return (redirect('register'))
            elif User.objects.filter(email=email).exists():
                print("This email is already registered")
                messages.info(request, "This email is already registered")
                return redirect('register')
            else:
                User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                         username=username, password=password)
                # save person to database
                People.objects.create(username=username, firstName=first_name, hashPass=hash(password))
                return render(request, 'homepage/login.html')
        else:
            print("Passwords do not match!")
            messages.info(request, "Passwords do not match")
            return redirect('register')
    else:
        return render(request, 'homepage/register.html')
