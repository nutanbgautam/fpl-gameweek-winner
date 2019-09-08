from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import *
import requests
import json
import time

#variables
page,line=1,1
a,results,session=None,None,None
players=[]
totalPlayers=0
playersDetail=None

def login(username,password):
    global session
    session = requests.session()
    loginUrl = 'https://users.premierleague.com/accounts/login/'
    payload = {
     'password': password,
     'login': username,
     'redirect_uri': 'https://fantasy.premierleague.com/a/login',
     'app': 'plfpl-web'
    }
    session.post(loginUrl, data=payload)

def getdata(leagueId):
    global results
    url="https://fantasy.premierleague.com/api/leagues-classic/"+str(leagueId)+"/standings/?page_standings="+str(page)
    # print("I am above session.get")
    response=session.get(url)
    # print("I am below session.get")
    data=response.text
    parsed=json.loads(data)
    try:
        results=parsed["standings"]["results"]
    except:
        results=None
    
def dataCollections(leagueId):
    global page,totalPlayers,line
    getdata(leagueId)
    while (results!=[]):
        getdata(leagueId)
        for i in results:
            a=[i["player_name"],i["event_total"],i["total"],i["last_rank"],page,line]
            players.append(a)
            totalPlayers=totalPlayers+1
            line=line+1
            a=[]
        line=1
        page=page+1
        
def sortingResults():
    global players
    def takeSecond(elem): # take second element for sort
        return elem[1]
    players.sort(key=takeSecond,reverse=True)

# def printingResult(timetaken):
#     print("Name =",players[0][0])
#     print("Gameweek Point =",players[0][1])
#     print("Total Point =",players[0][2])
#     print("Last time rank =",players[0][3])
#     print("At page number =",players[0][4],"and line =",players[0][5])
#     print("\nTotal Players = ",totalPlayers)
#     print("\nTime Consumed :",timetaken,"seconds")
    
def main(username,password,leagueId):
    # startTime=time.time()
    login(username,password)
    dataCollections(leagueId)
    sortingResults()
    link="https://fantasy.premierleague.com/leagues/"+str(leagueId)+"/standings/c?phase=1&page_new_entries=1&page_standings="+str(players[0][4])
    playersDetails={
        "first":{    "name" : players[0][0],
            "gwpoint" :players[0][1],
            "tpoint" :players[0][2],
            "lrank" :players[0][3],
            "pno" :players[0][4],
            "lno" :players[0][5],
            "link":link
        },
                "second":{    "name" : players[1][0],
            "gwpoint" :players[1][1],
            "tpoint" :players[1][2],
            "lrank" :players[1][3],
            "pno" :players[1][4],
            "lno" :players[1][5],

        },
                        "third":{    "name" : players[2][0],
            "gwpoint" :players[2][1],
            "tpoint" :players[2][2],
            "lrank" :players[2][3],
            "pno" :players[2][4],
            "lno" :players[2][5],

        },
                        "fourth":{    "name" : players[3][0],
            "gwpoint" :players[3][1],
            "tpoint" :players[3][2],
            "lrank" :players[3][3],
            "pno" :players[3][4],
            "lno" :players[3][5],

        },
                        "fifth":{    "name" : players[4][0],
            "gwpoint" :players[4][1],
            "tpoint" :players[4][2],
            "lrank" :players[4][3],
            "pno" :players[4][4],
            "lno" :players[4][5],

        }
    }
    return playersDetails
    # endTime=time.time()
    # timeTaken=endTime-startTime
    # printingResult(timeTaken)

def index(request):
    global playersDetail
    print("\n I am in index function \n")
    form=LeagueId()
    if playersDetail==None:
        # print("Player Detail is none so I rendered this \n")
        return render(request,"main.html",{'form':form})
    else:
        # print("Player Detail is not none \n")
        # print("Request here is ",request)
        # print("\n")
        return render(request,"main.html",{"totalPlayers":totalPlayers,"players1":playersDetail['first'],"players2":playersDetail['second'],"players3":playersDetail['third'],"players4":playersDetail['fourth'],"players5":playersDetail['fifth'],"form":form})

def getDatas(request):
    global totalPlayers,playersDetail
    form=LeagueId(request.POST or None)
    email=request.POST['email']
    password=request.POST['password']
    leagueId=request.POST['leagueId']
    # print("\nI am in getDatas\n")
    playersDetail=main(email,password,leagueId)
    # print("I posted in main function in getDatas\n")
    return HttpResponseRedirect("/")

