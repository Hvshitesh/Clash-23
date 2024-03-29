import app_1.views
from django.contrib.auth.models import User
from .models import Player
from datetime import date, timedelta, datetime
from django.utils import timezone
from django.shortcuts import redirect,HttpResponseRedirect

def check_time(view_fun):
    def wrap(request,*args, **kwargs):
        print("inside dec username",request.user.username)
        user = User.objects.get(username=request.user)
        player = Player.objects.get(user= user)
        EndTime = player.EndTime.astimezone()
        end_time = datetime(year=EndTime.year, month=EndTime.month, day=EndTime.day, hour=EndTime.hour, minute=EndTime.minute, second=EndTime.second)
        final_time = int(end_time.timestamp())   #user end time in sec
        current_time =  int(datetime.now().timestamp())   #crrent server time in sec
        print("end time ",final_time,EndTime)
        print("crnt time ",current_time,datetime.now())
        print("diff ",final_time-current_time)
        dif = final_time-current_time

        if (dif < 0):
            return app_1.views.submit(request)
            # return view_func(request,*args,**kwargs)
        else:
            return view_fun(request,*args,**kwargs)
                    
    return wrap

def check_test_ended(view_fun):
    def wrap(request,*args,**kwargs):
        if (request.user.is_authenticated):
            user = User.objects.get(username=request.user)
            player = Player.objects.get(user= user)
            if (player.isEnded):
                print("game is ended")
                print("iside decoratro to check going result in testcheck")
                return app_1.views.result(request)
                # return redirect('result')
                # return HttpResponseRedirect("result")
            else:
                print("game is not ended")

                return view_fun(request,*args,**kwargs)
        else:
            # return app_1.views.signin(request)
            return redirect("signin")
    return wrap


