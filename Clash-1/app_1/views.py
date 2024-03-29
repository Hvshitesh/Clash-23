from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
import re
from .utils import *
from django.http import JsonResponse
from datetime import datetime,timedelta
from .decorators import *
# from django.core.cache import cache
from django.views.decorators.cache import never_cache
from django.urls import reverse
import requests
# Create your views here.

from .addquestion import *
#Users home page after login
@never_cache
@login_required(login_url="signin")

def home(request):
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    context={
        "title":"Home",
        "user":request.user
    }
    if (player.isStarted):
        return redirect("questions")
    #To check checkbox is clicked or not
    if request.method == "POST":
        # user = User.objects.get(username=request.user)
        # player = Player.objects.get(user=user)
        checkbox = request.POST.get("checkbox") #It take value checked from frontend
        if (checkbox == "checked"):
            if not(player.isStarted):
                player.isStarted = True
                player_time_detail = set_time()
                player.startTime = player_time_detail["start_time"]
                player.EndTime = player_time_detail["end_time"]
                player.save()
            if (player.isEnded):
                return redirect("result")
            return redirect("questions")
        else:
            messages.error(request, "Checkbox not checked")
            return redirect("home")
    return render(request,"app_1/InstructionPage.html",context)


#It restrict user to go back from result to question page 
from django.views.decorators.cache import never_cache
@never_cache
@check_test_ended
@check_time
def questions(request):

    context={
        "title":"Questions",
        "flag":True
    }
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    
    #It handles user next question
    if "next" in request.POST:       
        u_option = request.POST.get("option")

        #This is for if submission is already given
        if len(Submission.objects.filter(player=player,questionID=player.questionNumber))>0:

            submission = Submission.objects.get(player=player,questionID=player.questionNumber) 
            submission.userOption = u_option
        else:
            submission = Submission(player=player,questionID=player.questionNumber,userOption=u_option,questionIndex=player.questionIndex)
            submission.save()


        #To get previous answer and its actual answer to give marks accordingly
        try:
            previous_answer = Submission.objects.get(player=player,questionID=player.previousQuestion).userOption
            actual_ans_prev_que= Question.objects.get(id=player.previousQuestion).questionAnswer  #to get actual answer of prev question
        except:
            previous_answer=None
            actual_ans_prev_que=None


        #To check marking scheme
        #check in utils
        marks_dict=get_question(json.loads(player.questionList),player.previousQuestion,previous_answer,actual_ans_prev_que)  
        #check in utils 
        user_answer_status=check_answer(u_option , Question.objects.get(id=player.questionNumber),marks_dict,player,user)  #it checks ans of crnt question
        
        #To save in player object
        player.playerScore += user_answer_status["score"]
        player.questionList=json.dumps(marks_dict["ques_list"])
        player.previousQuestion =  player.questionNumber 
        player.questionNumber = marks_dict["ques_number"]
        player.marksAdd=user_answer_status["marks_add_to_player"]
        player.marksSubstract=user_answer_status["marks_sub_to_player"]
        player.questionIndex +=1
        submission.points = user_answer_status["score"]
        submission.isCorrect=user_answer_status["isCorrect"]

        #To check if any lifeline is activate or not for that solved question 
        try:
            print("******************************")
            lifeline = Lifeline.objects.get(user=user,isActive=True)
            print("lifeline is activated",lifeline)
            if (lifeline.isActive):
                submission.lifelineActivated = True
                lifeline.isActive = False
                lifeline.save()
                player.lifelineActivationFlag = False
                array=json.loads(player.lifelineArray )
                print("player lifeline array",array)
                #This is clear all array as we are redirecting it to again on question so in get request it check outside next and nsubmit
                array.clear()
                print("player lifeline array after deletion",array)
                player.lifelineArray = json.dumps(array)
                player.save()
                print("****************************")
        except:
            #it is nessecory if user had not clicked any lifeline then for next lifeline lifeline 1 will be disable if it is activated
            # array=json.loads(player.lifelineArray )
            # if (1 in array):
            #     submission.lifelineActivated = True
            #     array.remove(1)
            # player.lifelineArray = json.dumps(array)
            # player.save()
            pass
            
        submission.save()
        player.save()
        return redirect("questions")

    #it handle users submit 
    if "nsubmit" in request.POST:
        u_option = request.POST.get("option")
        if len(Submission.objects.filter(player=player,questionID=player.questionNumber))>0:
            submission = Submission.objects.get(player=player,questionID=player.questionNumber)
            submission.userOption = u_option
            submission.save()
        else:
            submission = Submission(player=player,questionID=player.questionNumber,userOption=u_option,questionIndex=player.questionIndex)
            submission.save()
        return redirect("submit")
        
        
    #This may have to change as if the user used lifeline2 at last question btn visible to user is submit not next for last question
    if len(json.loads(player.questionList))<=0:
        print("printed when There is no question ",len(json.loads(player.questionList)))
        context["flag"]=False

    try:
        previous_submitions = Submission.objects.filter(player=player).all()
        life_line_dict = check_lifeline_activate(user,player,previous_submitions,Question.objects.get(id=player.questionNumber))
    except:
        life_line_dict = {"activate":False}

    #To show user which lifeline are activate now for them
    try:
        which_lifeline_is_active = Lifeline.objects.get(user=user,isActive=True)
        context["which_lifeline_is_active"]=which_lifeline_is_active
        if (which_lifeline_is_active.lifelineID== 3): 
            print(player.chatBotResponse)
            print(type(json.loads(player.chatBotResponse)))
            context["chatBotOutput"]=json.loads(player.chatBotResponse)
    except:
        pass
    context["life_line_dict"]=json.dumps(life_line_dict)
    print("**********************")
    print("activated lifelines ",context["life_line_dict"])
    print("*********************")
    
    # context["wrong_question_list"]=[x.questionIndex for x in Submission.objects.filter(player=player) if x.points<0]
    context["wrong_question_list"]=[x.questionIndex for x in Submission.objects.filter(player=player) if not(x.isCorrect)]

    print("Users Wrong questions ",context["wrong_question_list"])

    context["question"]=Question.objects.get(questionNumber=player.questionNumber,forJunior=player.isJunior)
    context["question_number"]=player.questionIndex
    
    context["player"]=player
    context["marking_scheme"]={"marks_add":player.marksAdd,"marks_sub":player.marksSubstract}
    context['player_time']=str(player.EndTime.astimezone())
    print("EndTime of user going to frontend ",player.EndTime.astimezone())

    context["playerStreak"]=checkStreak(player)
    return render(request,"app_1/MCQPage.html",context)
    # return render(request,"app_1/questions.html",context)



from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def lifelineActivation(request):
    if request.method == "POST":
        lifeline_id_from_frontend = request.POST.get("number")
        userr =request.POST.get("user")
        user = User.objects.get(username=userr)
        print(lifeline_id_from_frontend,"in url async")
        player=Player.objects.get(user=user)
        if(int(lifeline_id_from_frontend)==1):
            lifeline = Lifeline.objects.get(user=user,lifelineID=lifeline_id_from_frontend)
            lifeline.isActive = True
            lifeline.lifelineCounter +=1
            lifeline.save()
            return JsonResponse({"status":1})
        elif(int(lifeline_id_from_frontend)==2):
            #This is for when user uses 2nd lifline on question that will show him after lifeline use
            # arr = json.loads(player.questionList)
            # if not(player.questionNumber in arr):
            #     arr.append(player.questionNumber)
            #     player.questionList = json.dumps(arr)
            ques_num =int(request.POST.get("ques_num"))
            print(type(ques_num)," Type of question number comming from frontend")
            player.questionIndex -=1
            submission = Submission.objects.get(player=player,questionIndex=ques_num)
            question = Question.objects.get(id=submission.questionID)
            player.questionNumber=submission.questionID
            player.save()
            question_details={
                "question_title":question.questionText,
                "opt1":question.questionOption1,
                "opt2":question.questionOption2,
                "opt3":question.questionOption3,
                "opt4":question.questionOption4,
                "question_number":submission.questionIndex,
            }
            lifeline = Lifeline.objects.get(user=user,lifelineID=lifeline_id_from_frontend)
            lifeline.isActive = True
            lifeline.lifelineCounter +=1
            lifeline.save()
            return JsonResponse({"status":1,"question":question_details})
        elif(int(lifeline_id_from_frontend) == 3):
            print(type(request.POST.get("chatBotInput")))
            inputFromUser = request.POST.get("chatBotInput")
            chatBotOutput = json.loads(chatbot_response(inputFromUser))
            if (chatBotOutput["status"]==0):
                return JsonResponse({"status":0 , "chatBotOutput" : chatBotOutput["answer"]})
            lifeline = Lifeline.objects.get(user=user,lifelineID=lifeline_id_from_frontend)
            lifeline.isActive = True
            lifeline.lifelineCounter +=1
            lifeline.save()
            player.chatBotResponse = json.dumps({"input" : inputFromUser , "output" : chatBotOutput["answer"]})
            player.save()
            print(player.chatBotResponse)
            print(type(player.chatBotResponse))
            print(type(json.loads(player.chatBotResponse)))
            return JsonResponse({"status":1 , "chatBotOutput" : chatBotOutput["answer"]})
    else:
        return JsonResponse({"status":0})

# @check_time
@check_test_ended
def submit(request):
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    if player.isStarted:
        if player.isEnded:
            return redirect("result")
        # u_option = request.POST.get("option")
        #To save user's responce

        """When user\'s time is over test gets automatically 
         submitted at that time there is chances that for that question users submission object is not get created 
          so.... """
        try:
            submission = Submission.objects.get(player=player,questionID=player.questionNumber)
            u_option = submission.userOption
        except:
            submission = Submission(player=player,questionID=player.questionNumber)
            u_option=None

        
        try:
            previous_answer = Submission.objects.get(player=player,questionID=player.previousQuestion).userOption
            actual_ans_prev_que= Question.objects.get(id=player.previousQuestion).questionAnswer  #to get actual anser of prev question
        except:
            previous_answer=None
            actual_ans_prev_que=None
        
        marks_dict=get_question(json.loads(player.questionList),player.previousQuestion,previous_answer,actual_ans_prev_que)
        user_answer_status=check_answer(u_option,Question.objects.get(id=player.questionNumber),marks_dict,player,user)
        player.playerScore +=user_answer_status["score"]
        player.questionList=json.dumps(marks_dict["ques_list"])
        player.previousQuestion =  player.questionNumber 
        player.questionNumber = marks_dict["ques_number"]
        player.isEnded=True
        submission.points = user_answer_status["score"]
        submission.isCorrect=user_answer_status["isCorrect"]

        if (player.lifelineActivationFlag):
            submission.lifelineActivated = True
            player.lifelineActivationFlag = False

        player.save()
        submission.save()

        # return redirect(result)
        return HttpResponseRedirect("/result/")


@login_required(login_url="signin")
def result(request):
    context={
        "title":"Result",
    }
    player = Player.objects.get(user=request.user)
    
    if (player.tabSwitchCount >3):
        logout(request)
        submission = Submission.objects.filter(player=player)
        context["player"]=request.user
        context["userAttempt"]=player.questionIndex
        context["totalAttempt"]=len(submission)
        context["rightAttempt"]=len(submission.filter(isCorrect=True))
        context["maxStreak"]=player.maxStreak
        context["playerMarks"]=player.playerScore
        player.playerScore += player.maxStreak
        player.save()
        context["playerScore"]=player.playerScore
        if (player.isJunior):
            context["TotalQuestions"]=len(Question.objects.filter(forJunior=True))
        else:
            context["TotalQuestions"]=len(Question.objects.filter(forJunior=False))
        print("dsafsdf",context["TotalQuestions"])

        return render(request,"app_1/Result.html",context)

    if not(player.isEnded):
        return redirect("leaderboard")
    submission = Submission.objects.filter(player=player)
    context["player"]=request.user
    context["playerScore"]=player.playerScore
    context["userAttempt"]=player.questionIndex
    context["totalAttempt"]=len(submission)
    context["rightAttempt"]=len(submission.filter(isCorrect=True))
    context["maxStreak"]=player.maxStreak
    context["playerMarks"]=player.playerScore
    player.playerScore += player.maxStreak
    player.save()
    context["playerScore"]=player.playerScore
    if (player.isJunior):
        context["TotalQuestions"]=len(Question.objects.filter(forJunior=True))
    else:
        context["TotalQuestions"]=len(Question.objects.filter(forJunior=False))

    logout(request)
    return render(request,"app_1/Result.html",context)

@login_required(login_url="signin")
def LogoutClicked(request):
    user = User.objects.get(username=request.user)
    player = Player.objects.get(user=user)
    player.isEnded = True
    player.save()
    return redirect('result')

@never_cache
def signin(request):
    try:
        username = request.POST['username']
        user = User.objects.get(username=username)
        player = Player.objects.get(user=user)
        if (player.isStarted):
            logout(request)
            messages.error(request,"You have already started the test.")
            return redirect('signin')
    except:
        pass
        # add()
    # changeOPtion()

    # print(player.questionList)
    # check(Question.objects.all())
    # user=User.objects.get(username="me69")
    # player=Player.objects.get(user=user)
    # print(type(player.questionList))
    # print(type(json.loads(player.questionList)))
    if request.method == "POST":   #For signin page only username and pass1 taken
        username = request.POST['username']
        password = request.POST['password']
        isTeam = request.POST['isTeam']
        if isTeam == "True":
            isTeam = True
        else:
            isTeam = False
        print(isTeam, "isteam", type(isTeam))
        
        # print("isTEam ",isJunior,type(isJunior))
        user = authenticate(username=username, password= password)         #authenticate user here

        if user is not None :  #IF correct credentials given
            # player = Player.objects.get(user=user)
            try:
                player = Player.objects.get(user=user)
            except:
                player = Player(user=user)
                player.save()
                player = Player.objects.get(user=user)
            # print(player,player.isEnded)
            if not(player.isEnded) :
                login(request, user)
                # player = User.objects.get(username=request.user)
                # print(player.questionList)
               
                if not(player.questionList) or (player.questionList=="")  :
                    player.questionList = create_random_list(player.questionNumber,player.isJunior)
                    player.save()
                return redirect("home")
            else:
                messages.error(request,"You already given the test")

        else:  #If wrong credentials given on local server
            url = 'https://api.credenz.in/api/verify/user/'
            headers = {'Content-Type': 'application/json'}

            data = {
                'username': username,
                'password': password,
                'event': 'clash',
            }
            
            if isTeam:
                data['is_team'] = "true"
                print("here")
            else:
                data['is_team'] = None # empty string

            response = requests.post(url, headers=headers, json=data)
            

            if response.status_code == 200:
                response = response.json()
                user = User.objects.create_user(username=username, password=password, )
                if not isTeam:
                    try:
                        isJunior = not response['user']['senior']
                        first_name = response['user']['first_name']
                        last_name = response['user']['last_name']
                    except:
                        messages.error(request, "Invalid Credentials")
                        return redirect('signin')
                else: # if team
                    isJunior = True
                    first_name = response['users'][0]['first_name']
                    last_name = response['users'][0]['last_name']

                    # display name
                    display_name = ""
                    for user1 in response['users']:
                        display_name += user1['username'] + " &"
                        if user1['senior']:
                            isJunior = False
                    display_name = display_name[:-2]
                    print(display_name)
                            
                player = Player(user=user, isJunior=isJunior)
                player.questionList = create_random_list(player.questionNumber,player.isJunior)
                player.save()
                login(request, user)
                # messages.success(request, "Login Successful")
                return redirect("home")
            messages.error(request, "Bad Credentials")
            return redirect('signin')

    return render(request,"app_1/LoginPage.html")



# @login_required(login_url="signin")
def signout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully!")
        return redirect("signin")
    else:
        return redirect('signin')

def signup(request):
    
    if request.method == "POST": #Create user details to take them input
        # username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']  #For storing pass2
        isTeam = request.POST['isTeam']
        if User.objects.filter(username=username):
            messages.error(request,"Username already exists ! PLease try Different username")
            return redirect('home')

        if len(username)<3:
            messages.error(request,"Username must be atleast 3 characters")

        if pass1 != pass2:
            messages.error(request,"Passwords did not match")

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric")
            return redirect('home')

        if len(pass1)>8:
                if re.search('[A-Z]', pass1)!=None and re.search('[0-9]', pass1)!=None and re.search("^.*(?=.{8,})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=]).*$", pass1)!=None:
                    
                    myuser = User.objects.create_user(username, email, pass1) #register user in backend
                    myuser.first_name = fname
                    myuser.last_name = lname
                    player = Player(user=myuser,isJunior=isTeam)
                    player.save()
                    myuser.save() #save user in database
                    
                    messages.success(request, "Your account has been successfully created. We have sent you a confirmation email, please confirm your email in order to activate your account.")
                    return redirect('signin')
        else:
                messages.error(request, "Password must contain atleast one number, one  special character and one capital letter")
                return redirect('signup')

          
    #gives too many errors to redirect it on same page    
    # else:
    #     messages.error(request,"User Registration Failed")
    #     return redirect('signup')

    return render(request,"app_1/signup.html")






def leaderboard(request):
    context ={}
    # player.lifelineArray = json.dumps([1,2])
    # life_line_array = json.loads(player.lifelineArray)
    # submission=Submission.objects.filter(player=player).order_by("-id")[:3].values_list()
    # print(submission)

    # return render(request,"app_1/LoginPage.html")
    # return render(request,"app_1/MCQPage.html")
    # return render(request,"app_1/Result.html")
    # player = Player.objects.filter(playerScore__lt = 33).order_by("-playerScore")
    try:
        user = Player.objects.get(user=request.user)
        player = Player.objects.filter(isJunior=user.isJunior).order_by("-playerScore")
    except:
        player = Player.objects.filter(isJunior=True).order_by("-playerScore")

    # player = Player.objects.filter(isJunior=True).order_by("-playerScore")
    # print(player)
    l = json.dumps(getLeaderBoard(player))
    context["players"]=l
    try:
        if request.user.is_authenticated:
            context["player"] = Player.objects.get(user=request.user)
    except:
        pass
    
    # return render(request,"app_1/pag.html",context)
    return render(request,"app_1/LeaderBoard.html",context)

@csrf_exempt
def getJSLeaderboard(request):
    if (request.method == "POST"):
       isJunior = request.POST["isJunior"]
    #    print("Fsdffds",isJunior)
       player = Player.objects.filter(isJunior = isJunior).order_by("-playerScore")
       l = json.dumps(getLeaderBoard(player))
       return JsonResponse({"status":1,"player":l})



    


# def ipaddress(request):
#     # user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
#     # if user_ip:
#     #     ip = user_ip.split(',')[0]
#     # else:
#     #     ip = request.META.get('REMOTE_ADDR')
#     user_ip = request.META.get('REMOTE_ADDR')
    
#     # return HttpResponse("Welcome User!<br>You are visiting from: {}".format(ip))
#     return HttpResponse("Welcome User!<br>You are visiting from: {}".format(user_ip))



@csrf_exempt
def windowBlurError(request):
    username = request.POST.get("user")
    user = User.objects.get(username=username)
    player = Player.objects.get(user=user)
    print(player.tabSwitchCount)
    player.tabSwitchCount += 1
    player.save()
    return JsonResponse({'status':1,"tabSwitchValue":player.tabSwitchCount})


#To handle 404 error if user try to access diff page
def error_404(request, exception):
    return redirect('signin')
# def error_500(request):
#     return redirect('signin')
# def error_400(request,exception):
#     return redirect('signin')
# def error_403(request, exception):
#     return redirect('signin')


def webadmin(request) :
    
    if request.method == 'POST':
        superusername = request.POST['superusername']
        superpwd = request.POST['pass1']

        username = request.POST['username']
        timeIncrese = int(request.POST['time'])

        superuser = authenticate(username = superusername, password = superpwd)
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"user is not present")
            return redirect("webadmin")

        if superuser is not None and superuser.is_superuser:
            profile = Player.objects.get(user = user)
            profile.EndTime += timedelta(minutes=timeIncrese)

            profile.save()

            messages.success(request, "Updated")
            return render(request, "app_1/AdminPage.html")

        else:
            messages.error(request, "Bad Credentials")
            return render(request, "app_1/AdminPage.html")
        
    return render (request, "app_1/AdminPage.html")