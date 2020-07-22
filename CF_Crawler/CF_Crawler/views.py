from django.shortcuts import render
import urllib3
import json
from collections import Counter
from datetime import datetime
#from .forms import UserHandle
from django.http import HttpResponseRedirect


def main_page(request):
    context = {}
    return render(request, 'index.html', context)


def user_handle(request):
    # if this is a POST request we need to process the form data
    context1 = {}
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = request.POST['input_handle']

        http = urllib3.PoolManager()
        u = http.request('GET', ('https://codeforces.com/api/user.info?handles=' + form))
        userinfo_list = json.loads(u.data.decode('utf-8'))
        status = userinfo_list['status']
        if status != 'OK':
            print("user not found")
            status = False
            userinfo_list = userinfo_list['comment']
            print("yoyo " + userinfo_list)
        else:
            print("user found")
            status = True
            userinfo_list = userinfo_list["result"]
            userinfo_list = userinfo_list[0]
            tag = []
            lang = []
            verdict = []
            http = urllib3.PoolManager()
            u = http.request('GET', 'https://codeforces.com/api/user.status?handle=' + form)
            useranalysis = json.loads(u.data.decode('utf-8'))
            useranalysis = useranalysis["result"]
            for item in useranalysis:
                tag.extend(item['problem']['tags'])
            tagcount = Counter(tag)
            for item in useranalysis:
                lang.append(item['programmingLanguage'])
            langcount = Counter(lang)
            for item in useranalysis:
                verdict.append(item['verdict'])
            verdictcount = Counter(verdict)
            #---------------
            ok_submissions = []
            count=0
            for item in useranalysis:
                if item['verdict']=='OK':
                    ok_submissions.append(item['creationTimeSeconds'])
            print(ok_submissions)
            #---------------
            #rating
            rating =[]
            rtime = []
            rank=[]
            http = urllib3.PoolManager()
            u = http.request('GET', 'https://codeforces.com/api/user.rating?handle='+ form)
            useranalysis3 = json.loads(u.data.decode('utf-8'))
            useranalysis3 = useranalysis3["result"] 
            for item in useranalysis3:
                rating.append(item['newRating'])

            for item in useranalysis3:
                rtime.append(item['ratingUpdateTimeSeconds'])
            dtime=[]
            for i in rtime:
                dtime.append(datetime.fromtimestamp(i).strftime("%d %b'%y"))
            
            #   print(dtime)
            context1 = {'userinfo_list': userinfo_list, 'status': status,'tagcount': tagcount,'langcount':langcount,'dtime':dtime, 'rating':rating,'verdictcount':verdictcount}
            # return HttpResponseRedirect('/userhandle')
    else:
        form = UserHandle()
    return render(request, 'userinfo.html', context1)
